import json
from adopts.factories import AdoptFactory
from adopts.models import Adopt
from colors.factories import ColorPoolFactory
from colors.models import ColorPool, Color, ColorPalette
from colors.serializers import ColorPoolSerializer
from django.conf import settings
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


class ColorPoolSerializerTests(TestCase):
    def test_serializes(self):
        color_pool = ColorPoolFactory()
        self.assertEqual(ColorPoolSerializer(color_pool).data, {
            'id': color_pool.id,
            'name': color_pool.name,
            'date_updated': color_pool.date_updated.strftime(settings.DATETIME_FORMAT),
            'colors': color_pool.colors,
            'colors_json': color_pool.colors_json(),
        })


class ColorFromDbTests(TestCase):
    def test_fails_with_no_input(self):
        with self.assertRaises(AssertionError) as context:
            Color.from_db('')

    def test_fails_with_no_name(self):
        with self.assertRaises(AssertionError) as context:
            Color.from_db('#ccc #000 #fff')

    def test_builds_single_color(self):
        colors = Color.from_db('color1 #ccc #000 #fff')
        self.assertEqual(1, len(colors))
        self.assertIsInstance(colors[0], Color)
        self.assertEqual('color1', colors[0].name)
        self.assertIsInstance(colors[0].palettes, list)
        self.assertIsInstance(colors[0].palettes[0], ColorPalette)
        self.assertEqual('#ccc', colors[0].palettes[0].base)
        self.assertEqual('#000', colors[0].palettes[0].shading)
        self.assertEqual('#fff', colors[0].palettes[0].highlight)

    def test_builds_multiple_palettes(self):
        colors = Color.from_db('color1 #aaa #aab #aac #aba #abb #abc')
        self.assertEqual(1, len(colors))
        self.assertEqual('color1', colors[0].name)
        self.assertEqual(('#aaa', '#aab', '#aac'), (
            colors[0].palettes[0].base, colors[0].palettes[0].shading, colors[0].palettes[0].highlight))
        self.assertEqual(('#aba', '#abb', '#abc'), (
            colors[0].palettes[1].base, colors[0].palettes[1].shading, colors[0].palettes[1].highlight))

    def test_builds_multiple_colors(self):
        colors = Color.from_db(
            'color1 #aaa #aab #aac #aba #abb #abc\ncolor2 #baa #bab #bac #bba #bbb #bbc\ncolor3 #ca1 #cb1 #cc1 #ca1 #cb2 #cc3')
        self.assertEqual(3, len(colors))
        self.assertEqual('color1', colors[0].name)
        self.assertEqual(2, len(colors[0].palettes))
        self.assertEqual('color2', colors[1].name)
        self.assertEqual(2, len(colors[1].palettes))
        self.assertEqual('color3', colors[2].name)
        self.assertEqual(2, len(colors[2].palettes))


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
            ColorPoolSerializer(color_pool_1).data,
            ColorPoolSerializer(color_pool_2).data,
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
        color_pool = adopt.color_pools.filter(name='Foo', colors='foo').get()
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
            id=color_pool.id, name='Foo', colors='foo').get()
        self.assertEqual(response.data, ColorPoolSerializer(color_pool).data)

    def test_fails_when_unauthorized(self):
        user = UserFactory()
        adopt = AdoptFactory()
        color_pool = ColorPoolFactory(adopt=adopt)

        response = self._put(color_pool, user=user)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(adopt.color_pools.filter(
            id=color_pool.id, name='Foo', colors='foo').exists(), False)


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

        self.assertEqual(response.status_code, 202)
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
