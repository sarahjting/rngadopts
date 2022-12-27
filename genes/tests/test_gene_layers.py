from adopts.factories import AdoptFactory
from colors.factories import ColorPoolFactory
from genes.factories import GeneFactory, GeneLayerFactory, GenePoolFactory
from genes.serializers import GeneSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from genes.models import Gene, GeneLayer
from rest_framework.test import APIClient
from users.factories import UserFactory


def gene_layers_endpoint(obj):
    if isinstance(obj, Gene):
        return reverse('genes:layers_api', kwargs={'adopt_id': obj.gene_pool.adopt_id})
    elif isinstance(obj, GeneLayer):
        return reverse('genes:layers_api', kwargs={'adopt_id': obj.gene.gene_pool.adopt_id, 'pk': obj.id})
    else:
        raise ValueError('Invalid gene endpoint.')


class GeneLayerApiCreateTests(TestCase):
    def _post(self, gene, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.post(gene_layers_endpoint(gene), {
            'gene_id': gene.id,
            'type': 'static_over',
            # single black pixel
            'image': SimpleUploadedFile('foo.gif', b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif'),
        } | data)

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._post(gene)

        self.assertEqual(response.status_code, 403)

    def test_creates(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        color_pool = ColorPoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._post(gene, user=user, data={
                              'color_pool_id': color_pool.id})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, gene.gene_layers.count())

    def test_fails_when_invalid_image(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._post(gene, user=user, data={
                              'image': SimpleUploadedFile('foo.gif', b'foo', content_type='application/json')})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(0, gene.gene_layers.count())

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)

        response = self._post(gene, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(0, adopt.adopt_layers.count())


class GeneLayerApiUpdateTests(TestCase):
    def _update(self, gene_layer, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.patch(gene_layers_endpoint(gene_layer), {'sort': 10} | data)

    def test_fails_when_unauthenticated(self):
        gene_layer = GeneLayerFactory()
        response = self._update(gene_layer)
        self.assertEqual(response.status_code, 403)

    def test_updates(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)
        gene_layer = GeneLayerFactory(gene=gene)

        response = self._update(gene_layer, user=user, data={
                                'color_pool_id': color_pool.id})
        gene_layer.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, gene_layer.sort)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)
        gene_layer = GeneLayerFactory(gene=gene)

        response = self._update(gene_layer, user=user)
        gene_layer.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(0, gene_layer.sort)


class GeneApiDeleteTests(TestCase):
    def _delete(self, gene_layer, user=None):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.delete(gene_layers_endpoint(gene_layer))

    def test_fails_when_unauthenticated(self):
        gene_layer = GeneLayerFactory()
        response = self._delete(gene_layer)
        self.assertEqual(response.status_code, 403)

    def test_deletes(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)
        gene_layer = GeneLayerFactory(gene=gene)

        response = self._delete(gene_layer, user=user)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(gene.gene_layers.count(), 0)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        gene_pool = GenePoolFactory(adopt=adopt)
        gene = GeneFactory(gene_pool=gene_pool)
        gene_layer = GeneLayerFactory(gene=gene)

        response = self._delete(gene_layer, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(gene.gene_layers.count(), 1)
