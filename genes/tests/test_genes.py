from adopts.factories import AdoptFactory
from adopts.serializers import AdoptListSerializer
from colors.factories import ColorPoolFactory
from genes.factories import GeneFactory, GenePoolFactory
from genes.serializers import GenePoolListSerializer, GeneSerializer, GeneListSerializer
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from genes.models import Gene, GenePool
from rest_framework.test import APIClient
from users.factories import UserFactory


def gene_endpoint(obj):
    if isinstance(obj, GenePool):
        return reverse("genes:api", kwargs={"adopt_id": obj.adopt_id, "gene_pool_id": obj.id})
    elif isinstance(obj, Gene):
        return reverse("genes:api", kwargs={"adopt_id": obj.gene_pool.adopt_id, "gene_pool_id": obj.gene_pool_id, "pk": obj.id})
    else:
        raise ValueError("Invalid gene endpoint.")


class GeneSerializerTest(TestCase):
    def test_serializes(self):
        gene = GeneFactory()
        self.assertEqual(GeneSerializer(gene).data, {
            "id": gene.id,
            "adopt": AdoptListSerializer(gene.adopt).data,
            "gene_pool": GenePoolListSerializer(gene.gene_pool).data,
            "has_color": gene.has_color,
            "color_pool_id": None,
            "color_pool": None,
            "name": gene.name,
            "slug": gene.slug,
            "weight": gene.weight,
            "date_updated": gene.date_updated.strftime(settings.DATETIME_FORMAT),
            "gene_layers": [],
        })


class GeneListSerializerTest(TestCase):
    def test_serializes(self):
        gene = GeneFactory()
        self.assertEqual(GeneListSerializer(gene).data, {
            "id": gene.id,
            "color_pool": None,
            "name": gene.name,
            "slug": gene.slug,
            "weight": gene.weight,
            "date_updated": gene.date_updated.strftime(settings.DATETIME_FORMAT),
            "gene_layers": [],
        })


class GeneApiIndexTests(TestCase):

    def _get(self, gene_pool, user=None):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.get(gene_endpoint(gene_pool))

    def test_fails_when_unauthenticated(self):
        gene_pool = GenePoolFactory()
        response = self._get(gene_pool)
        self.assertEqual(response.status_code, 403)

    def test_sees_no_genes(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)

        response = self._get(gene_pool, user=user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_sees_authorized_gene_pools(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)

        gene_2 = GeneFactory(name="Z", gene_pool=gene_pool)
        gene_1 = GeneFactory(name="A", gene_pool=gene_pool)
        gene_deleted = GeneFactory(
            gene_pool=gene_pool, date_deleted=timezone.now())

        response = self._get(gene_pool, user=user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            GeneListSerializer(gene_1).data,
            GeneListSerializer(gene_2).data,
        ])

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)

        response = self._get(gene_pool, user=user)

        self.assertEqual(response.status_code, 403)

    def test_fails_for_invalid_gene_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)

        unrelated_adopt = AdoptFactory(mods=(user,))

        client = APIClient()
        response = client.get(reverse("genes:api", kwargs={
                              "adopt_id": unrelated_adopt.id, "gene_pool_id": gene_pool.id}))

        self.assertEqual(response.status_code, 403)


class GeneApiCreateTests(TestCase):
    def _post(self, gene_pool, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.post(gene_endpoint(gene_pool), {
            "name": "Foo",
            "slug": "foo",
            "has_color": True,
            "gene_pool_id": gene_pool.id,
            "color_pool_id": "",
            "weight": 1,
        } | data)

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)

        res = self._post(gene_pool)

        self.assertEqual(res.status_code, 403)

    def test_creates_gene(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        color_pool = ColorPoolFactory(adopt=adopt)

        res = self._post(gene_pool, user=user, data={
                         "color_pool_id": color_pool.id})

        self.assertEqual(res.status_code, 201)
        gene = Gene.objects.filter(
            name="Foo", slug="foo", gene_pool_id=gene_pool.id, color_pool_id=color_pool.id, weight=1).get()
        self.assertEqual(res.data, GeneSerializer(gene).data)

    def test_fails_with_nonunique_slug(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        color_pool = ColorPoolFactory(adopt=adopt)

        other_gene = GeneFactory(gene_pool=gene_pool, slug="foo")

        res = self._post(gene_pool, user=user, data={"slug": "foo"})

        self.assertEqual(res.status_code, 400)

    def test_creates_with_unique_slug_within_gene_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        color_pool = ColorPoolFactory(adopt=adopt)

        other_gene_pool = GenePoolFactory(adopt=adopt)
        other_gene = GeneFactory(gene_pool=other_gene_pool, slug="foo")

        res = self._post(gene_pool, user=user, data={"slug": "foo"})

        self.assertEqual(res.status_code, 201)


class GeneApiUpdateTests(TestCase):
    def _update(self, gene, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.put(gene_endpoint(gene), {
            "name": "Foo",
            "slug": "foo",
            "weight": 10,
            "color_pool_id": gene.color_pool_id or "",
            "has_color": True,
        } | data)

    def test_fails_when_unauthenticated(self):
        gene = GeneFactory()

        response = self._update(gene)

        self.assertEqual(response.status_code, 403)

    def test_updates_gene(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._update(gene, user=user, data={
                                "color_pool_id": color_pool.id})

        self.assertEqual(response.status_code, 200)

        gene = Gene.objects.filter(
            id=gene.id, gene_pool_id=gene_pool.id, name="Foo", slug="foo", weight=10, color_pool_id=color_pool.id).get()
        self.assertEqual(response.data, GeneSerializer(gene).data)

    def test_does_not_update_invalid_color_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        invalid_color_pool = ColorPoolFactory()
        response = self._update(gene, user=user, data={
                                "color_pool_id": invalid_color_pool.id})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Gene.objects.filter(
            id=gene.id, name="Foo").exists(), False)

    def test_does_not_update_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._update(gene, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Gene.objects.filter(
            id=gene.id, name="Foo").exists(), False)

    def test_fails_with_nonunique_slug(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        other_gene = GeneFactory(gene_pool=gene_pool, slug="foo")

        response = self._update(gene, user=user, data={"slug": "foo"})

        self.assertEqual(response.status_code, 400)

    def test_succeeds_with_unique_slug_within_gene_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        other_gene_pool = GenePoolFactory(adopt=adopt)
        other_gene = GeneFactory(gene_pool=other_gene_pool, slug="foo")

        response = self._update(gene, user=user, data={"slug": "foo"})

        self.assertEqual(response.status_code, 200)


class GeneApiDeleteTests(TestCase):

    def _delete(self, gene_pool, user=None):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.delete(gene_endpoint(gene_pool))

    def test_fails_when_unauthenticated(self):
        gene = GeneFactory()
        response = self._delete(gene)
        self.assertEqual(response.status_code, 403)

    def test_deletes_color_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._delete(gene, user=user)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Gene.objects.filter(
            id=gene.id).exclude(date_deleted=None).count(), 1)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._delete(gene, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Gene.objects.filter(
            id=gene.id, date_deleted=None).count(), 1)
