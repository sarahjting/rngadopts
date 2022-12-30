from adopts.factories import AdoptFactory
from adopts.models import Adopt
from colors.factories import ColorPoolFactory
from colors.serializers import ColorPoolListSerializer
from adopts.serializers import AdoptListSerializer
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from genes.factories import GenePoolFactory
from genes.models import GenePool
from genes.serializers import GenePoolSerializer, GenePoolListSerializer
from rest_framework.test import APIClient
from users.factories import UserFactory


def gene_pool_endpoint(obj):
    if isinstance(obj, Adopt):
        return reverse('genes:pool_api', kwargs={'adopt_id': obj.id})
    elif isinstance(obj, GenePool):
        return reverse('genes:pool_api', kwargs={'adopt_id': obj.adopt_id, 'pk': obj.id})
    else:
        raise ValueError('Invalid gene pool endpoint.')


class GenePoolSerializerTests(TestCase):
    def test_serializes(self):
        gene_pool = GenePoolFactory()
        self.assertEqual(GenePoolSerializer(gene_pool).data, {
            'id': gene_pool.id,
            'color_pool_id': gene_pool.color_pool_id,
            'color_pool': ColorPoolListSerializer(gene_pool.color_pool).data,
            'name': gene_pool.name,
            'type': gene_pool.type,
            'genes_count': gene_pool.genes_count,
            'genes_weight_total': gene_pool.genes_weight_total,
            'date_updated': gene_pool.date_updated.strftime(settings.DATETIME_FORMAT),
            'adopt': AdoptListSerializer(gene_pool.adopt).data,
        })


class GenePoolListSerializerTests(TestCase):
    def test_serializes(self):
        gene_pool = GenePoolFactory()
        self.assertEqual(GenePoolListSerializer(gene_pool).data, {
            'id': gene_pool.id,
            'color_pool': ColorPoolListSerializer(gene_pool.color_pool).data,
            'name': gene_pool.name,
            'type': gene_pool.type,
            'genes_count': gene_pool.genes_count,
            'genes_weight_total': gene_pool.genes_weight_total,
            'date_updated': gene_pool.date_updated.strftime(settings.DATETIME_FORMAT),
        })


class GenePoolApiIndexTests(TestCase):

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        client = APIClient()
        response = client.get(gene_pool_endpoint(adopt))
        self.assertEqual(response.status_code, 403)

    def test_sees_no_gene_pools(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        client = APIClient()
        client.force_login(user)
        response = client.get(gene_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_sees_authorized_gene_pools(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        client = APIClient()
        client.force_login(user)

        gene_pool_2 = GenePoolFactory(name='Z', adopt=adopt)
        gene_pool_1 = GenePoolFactory(name='A', adopt=adopt)
        gene_pool_deleted = GenePoolFactory(
            adopt=adopt, date_deleted=timezone.now())

        response = client.get(gene_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            GenePoolListSerializer(gene_pool_1).data,
            GenePoolListSerializer(gene_pool_2).data,
        ])

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()

        client = APIClient()
        client.force_login(user)

        response = client.get(gene_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 403)


class GenePoolApiCreateTests(TestCase):

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()

        client = APIClient()
        response = client.post(gene_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 403)

    def test_creates_gene_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)

        client = APIClient()
        client.force_login(user)

        response = client.post(gene_pool_endpoint(adopt), {
            'name': 'Foo',
            'type': 'basic',
            'adopt_id': adopt.id,
            'color_pool_id': color_pool.id,
        })

        self.assertEqual(response.status_code, 201)
        gene_pool = GenePool.objects.filter(
            name='Foo', adopt_id=adopt.id, type='basic', color_pool_id=color_pool.id).get()
        self.assertEqual(response.data, GenePoolSerializer(gene_pool).data)


class GenePoolApiUpdateTests(TestCase):

    def _update(self, gene_pool, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.put(gene_pool_endpoint(gene_pool), {
            'name': 'Foo',
            'type': 'multi',
            'color_pool_id': gene_pool.color_pool_id,
        } | data)

    def test_fails_when_unauthenticated(self):
        gene_pool = GenePoolFactory()

        response = self._update(gene_pool)

        self.assertEqual(response.status_code, 403)

    def test_updates_gene_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)
        gene_pool = GenePoolFactory(adopt=adopt, color_pool=color_pool)

        response = self._update(gene_pool, user=user)

        self.assertEqual(response.status_code, 200)

        gene_pool = GenePool.objects.filter(
            id=gene_pool.id, adopt_id=adopt.id, name='Foo', type='multi', color_pool_id=color_pool.id).get()
        self.assertEqual(response.data, GenePoolSerializer(gene_pool).data)

    def test_does_not_update_invalid_color_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)
        gene_pool = GenePoolFactory(adopt=adopt, color_pool=color_pool)

        invalid_color_pool = ColorPoolFactory()
        response = self._update(gene_pool, user=user, data={
                                'color_pool_id': invalid_color_pool.id})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(adopt.gene_pools.filter(
            id=gene_pool.id, name='Foo').exists(), False)

    def test_does_not_update_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        color_pool = ColorPoolFactory(adopt=adopt)
        gene_pool = GenePoolFactory(adopt=adopt, color_pool=color_pool)

        response = self._update(gene_pool, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(adopt.gene_pools.filter(
            id=gene_pool.id, name='Foo').exists(), False)


class GenePoolApiDeleteTests(TestCase):

    def _delete(self, gene_pool, user=None):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.delete(gene_pool_endpoint(gene_pool))

    def test_fails_when_unauthenticated(self):
        gene_pool = GenePoolFactory()
        response = self._delete(gene_pool)
        self.assertEqual(response.status_code, 403)

    def test_deletes_color_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)

        response = self._delete(gene_pool, user=user)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(GenePool.objects.filter(
            id=gene_pool.id).exclude(date_deleted=None).count(), 1)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)

        response = self._delete(gene_pool, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(GenePool.objects.filter(
            id=gene_pool.id, date_deleted=None).count(), 1)
