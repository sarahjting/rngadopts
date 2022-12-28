from adopts.factories import AdoptFactory, AdoptLayerFactory
from colors.factories import ColorPoolFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.factories import UserFactory


class AdoptLayerApiCreateTests(TestCase):

    def _post(self, adopt, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.post(reverse('adopts:layers_api', kwargs={'adopt_id': adopt.id}), {
            'type': 'static',
            # single black pixel
            'image': SimpleUploadedFile('foo.gif', b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif'),
        } | data)

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        response = self._post(adopt)
        self.assertEqual(response.status_code, 403)

    def test_creates(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)

        response = self._post(adopt, user=user, data={
                              'color_pool_id': color_pool.id})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, adopt.adopt_layers.count())

    def test_fails_when_invalid_image(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        response = self._post(adopt, user=user, data={
                              'image': SimpleUploadedFile('foo.gif', b'foo', content_type='application/json')})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(0, adopt.adopt_layers.count())

    def test_fails_when_invalid_color_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory()

        response = self._post(adopt, user=user, data={
                              'color_pool_id': color_pool.id})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(0, adopt.adopt_layers.count())

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()

        response = self._post(adopt, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(0, adopt.adopt_layers.count())


class AdoptLayerApiUpdateTests(TestCase):
    def _patch(self, adopt_layer, user=None):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.patch(reverse('adopts:layers_api', kwargs={'adopt_id': adopt_layer.adopt_id, 'pk': adopt_layer.id}), {
            'sort': 1
        })

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        adopt_layer = AdoptLayerFactory(adopt=adopt)

        response = self._patch(adopt_layer)
        adopt_layer.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(0, adopt_layer.sort)

    def test_updates(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        adopt_layer = AdoptLayerFactory(adopt=adopt)

        response = self._patch(adopt_layer, user=user)
        adopt_layer.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, adopt_layer.sort)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        adopt_layer = AdoptLayerFactory(adopt=adopt)

        response = self._patch(adopt_layer, user=user)
        adopt_layer.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(0, adopt_layer.sort)


class AdoptLayerApiDeleteTests(TestCase):
    def _delete(self, adopt_layer, user=None):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.delete(reverse('adopts:layers_api', kwargs={'adopt_id': adopt_layer.adopt_id, 'pk': adopt_layer.id}))

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        adopt_layer = AdoptLayerFactory(adopt=adopt)

        response = self._delete(adopt_layer)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(1, adopt.adopt_layers.count())

    def test_deletes(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        adopt_layer = AdoptLayerFactory(adopt=adopt)

        response = self._delete(adopt_layer, user=user)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, adopt.adopt_layers.count())

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        adopt_layer = AdoptLayerFactory(adopt=adopt)

        response = self._delete(adopt_layer, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(1, adopt.adopt_layers.count())
