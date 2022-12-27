from adopts.factories import AdoptFactory, AdoptLayerFactory
from adopts.models import Adopt
from adopts.serializers import AdoptSerializer, AdoptListSerializer
from colors.factories import ColorPoolFactory
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from users.factories import UserFactory


class AdoptSerializerTests(TestCase):
    def test_serializes(self):
        adopt = AdoptFactory()
        self.assertEqual(AdoptSerializer(adopt).data, {
            'id': adopt.id,
            'name': adopt.name,
            'short_name': adopt.short_name,
            'logs_count': 0,
            'layers_count': 0,
            'genes_count': 0,
            'date_updated': adopt.date_updated.strftime(settings.DATETIME_FORMAT),
            'adopt_layers': []
        })


class AdoptListSerializerTests(TestCase):
    def test_serializes(self):
        adopt = AdoptFactory()
        self.assertEqual(AdoptListSerializer(adopt).data, {
            'id': adopt.id,
            'name': adopt.name,
            'short_name': adopt.short_name,
            'logs_count': 0,
            'layers_count': 0,
            'genes_count': 0,
            'date_updated': adopt.date_updated.strftime(settings.DATETIME_FORMAT),
        })


class AdoptApiIndexTests(TestCase):

    def test_fails_when_unauthenticated(self):
        client = APIClient()
        response = client.get(reverse('adopts:api'))
        self.assertEqual(response.status_code, 403)

    def test_sees_no_adopts(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        response = client.get(reverse('adopts:api'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_sees_my_adopts(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        adopt_2 = AdoptFactory(name='Z', mods=(user,))
        adopt_1 = AdoptFactory(name='A', mods=(user,))
        adopt_deleted = AdoptFactory(mods=(user,), date_deleted=timezone.now())

        response = client.get(reverse('adopts:api'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            AdoptListSerializer(adopt_1).data,
            AdoptListSerializer(adopt_2).data,
        ])

    def test_do_not_see_adopts_that_are_not_mine(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        unrelated_user = UserFactory()
        unrelated_adopt = AdoptFactory(mods=(unrelated_user,))

        response = client.get(reverse('adopts:api'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])


class AdoptApiCreateTests(TestCase):
    def _post(self, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.post(reverse('adopts:api'), {
            'name': 'Foo',
            'short_name': 'foo',
        } | data)

    def test_fails_when_unauthenticated(self):
        response = self._post()
        self.assertEqual(response.status_code, 403)

    def test_fails_when_setting_disabled(self):
        settings.RNGADOPTS_ADOPT_CREATION_ENABLED = False

        user = UserFactory()
        response = self._post(user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(user.adopts.count(), 0)

    def test_creates_adopt(self):
        user = UserFactory()
        response = self._post(user)

        self.assertEqual(response.status_code, 201)
        adopt = user.adopts.filter(name='Foo', short_name='foo').get()
        self.assertEqual(response.data, AdoptSerializer(adopt).data)

    def test_fails_when_slug_nonunique(self):
        user = UserFactory()
        other_adopt = AdoptFactory(short_name='foo')

        response = self._post(user)

        self.assertEqual(response.status_code, 403)


class AdoptApiViewTests(TestCase):

    def _get(self, adopt, user=None):
        client = APIClient()
        if user:
            client.force_login(user)
        return client.get(reverse('adopts:api', kwargs={'pk': adopt.id}))

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        response = self._get(adopt)
        self.assertEqual(response.status_code, 403)

    def test_updates_my_adopt(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        response = self._get(adopt, user=user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, AdoptSerializer(adopt).data)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()

        response = self._get(adopt, user=user)

        self.assertEqual(response.status_code, 404)


class AdoptApiUpdateTests(TestCase):

    def test_fails_when_unauthenticated(self):
        client = APIClient()

        adopt = AdoptFactory()
        response = client.put(reverse('adopts:api'), kwargs={'pk': adopt.id})
        self.assertEqual(response.status_code, 403)

    def test_updates_my_adopt(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        adopt = AdoptFactory(mods=(user,))

        response = client.put(reverse('adopts:api', kwargs={'pk': adopt.id}), {
                              'name': 'Foo', 'short_name': 'foo'})

        self.assertEqual(response.status_code, 200)

        adopt = user.adopts.filter(
            id=adopt.id, name='Foo', short_name='foo').get()
        self.assertEqual(response.data, AdoptSerializer(adopt).data)

    def test_does_not_update_other_adopts(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        unrelated_user = UserFactory()
        unrelated_adopt = AdoptFactory(mods=(unrelated_user,))

        response = client.put(reverse('adopts:api', kwargs={'pk': unrelated_adopt.id}),  {
                              'name': 'Foo', 'short_name': 'foo'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(user.adopts.filter(
            id=unrelated_adopt.id, name='Foo', short_name='foo').count(), 0)


class AdoptApiDeleteTests(TestCase):

    def test_fails_when_unauthenticated(self):
        client = APIClient()
        response = client.delete(reverse('adopts:api'))
        self.assertEqual(response.status_code, 403)

    def test_deletes(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        adopt = AdoptFactory(mods=(user,))

        response = client.delete(
            reverse('adopts:api', kwargs={'pk': adopt.id}))

        self.assertEqual(response.status_code, 202)
        self.assertEqual(user.adopts.filter(
            id=adopt.id).exclude(date_deleted=None).count(), 1)

    def test_does_not_delete_other_adopts(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        unrelated_user = UserFactory()
        unrelated_adopt = AdoptFactory(mods=(unrelated_user,))

        response = client.delete(
            reverse('adopts:api', kwargs={'pk': unrelated_adopt.id}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Adopt.objects.filter(
            id=unrelated_adopt.id, date_deleted=None).count(), 1)


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
