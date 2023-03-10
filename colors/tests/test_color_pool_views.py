from adopts.factories import AdoptFactory
from adopts.models import Adopt
from colors.factories import ColorPoolFactory
from colors.models import ColorPool
from colors.serializers import ColorPoolListSerializer, ColorPoolSerializer
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from users.factories import UserFactory


def color_pool_endpoint(obj):
    if isinstance(obj, Adopt):
        return reverse('colors:api', kwargs={'adopt_id': obj.id})
    elif isinstance(obj, ColorPool):
        return reverse('colors:api', kwargs={'adopt_id': obj.adopt_id, 'pk': obj.id})
    else:
        raise ValueError('Invalid color pool endpoint.')


class ColorPoolApiIndexTests(TestCase):

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        client = APIClient()
        response = client.get(color_pool_endpoint(adopt))
        self.assertEqual(response.status_code, 403)

    def test_sees_no_color_pools(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        client = APIClient()
        client.force_login(user)
        response = client.get(color_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_sees_authorized_color_pools(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        client = APIClient()
        client.force_login(user)

        color_pool_2 = ColorPoolFactory(name='Z', adopt=adopt)
        color_pool_1 = ColorPoolFactory(name='A', adopt=adopt)
        color_pool_deleted_deleted = ColorPoolFactory(
            adopt=adopt, date_deleted=timezone.now())

        response = client.get(color_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            ColorPoolListSerializer(color_pool_1).data,
            ColorPoolListSerializer(color_pool_2).data,
        ])

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()

        client = APIClient()
        client.force_login(user)

        response = client.get(color_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 403)


class ColorPoolApiCreateTests(TestCase):

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()

        client = APIClient()
        response = client.post(color_pool_endpoint(adopt))

        self.assertEqual(response.status_code, 403)

    def test_creates_color_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        client = APIClient()
        client.force_login(user)

        response = client.post(color_pool_endpoint(adopt), {
            'name': 'Foo',
            'colors': 'foo',
            'adopt': adopt.id,
        })

        self.assertEqual(response.status_code, 201)
        color_pool = adopt.color_pools.filter(
            name='Foo', colors='foo foo').get()
        self.assertEqual(response.data, ColorPoolSerializer(color_pool).data)


class ColorPoolApiUpdateTests(TestCase):
    def _put(self, color_pool, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.put(color_pool_endpoint(color_pool), {
            'name': 'Foo',
            'colors': 'foo',
        } | data)

    def test_fails_when_unauthenticated(self):
        color_pool = ColorPoolFactory()
        response = self._put(color_pool)
        self.assertEqual(response.status_code, 403)

    def test_updates_color_pool(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)

        response = self._put(color_pool, user=user)

        self.assertEqual(response.status_code, 200)

        color_pool = adopt.color_pools.filter(
            id=color_pool.id, name='Foo', colors='foo foo').get()
        self.assertEqual(response.data, ColorPoolSerializer(color_pool).data)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        color_pool = ColorPoolFactory(adopt=adopt)

        response = self._put(color_pool, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(adopt.color_pools.filter(
            id=color_pool.id, name='Foo').exists(), False)


class ColorPoolApiDeleteTests(TestCase):

    def test_fails_when_unauthenticated(self):
        color_pool = ColorPoolFactory()

        client = APIClient()
        response = client.delete(color_pool_endpoint(color_pool))

        self.assertEqual(response.status_code, 403)

    def test_deletes_color_pools(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))
        color_pool = ColorPoolFactory(adopt=adopt)

        client = APIClient()
        client.force_login(user)

        response = client.delete(color_pool_endpoint(color_pool))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(ColorPool.objects.filter(
            id=color_pool.id).exclude(date_deleted=None).count(), 1)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        color_pool = ColorPoolFactory(adopt=adopt)

        client = APIClient()
        client.force_login(user)

        response = client.delete(color_pool_endpoint(color_pool))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(ColorPool.objects.filter(
            id=color_pool.id, date_deleted=None).count(), 1)
