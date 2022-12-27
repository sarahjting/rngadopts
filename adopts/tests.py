from adopts.factories import AdoptFactory
from adopts.models import Adopt
from adopts.serializers import AdoptSerializer
from django.conf import settings
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
            'count': 0,
            'date_updated': adopt.date_updated.strftime(settings.DATETIME_FORMAT),
        })


class AdoptApiIndexTests(TestCase):

    def test_fails_when_not_authenticated(self):
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
            AdoptSerializer(adopt_1).data,
            AdoptSerializer(adopt_2).data,
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

    def test_fails_when_not_authenticated(self):
        client = APIClient()
        response = client.post(reverse('adopts:api'))
        self.assertEqual(response.status_code, 403)

    def test_fails_when_setting_disabled(self):
        settings.RNGADOPTS_ADOPT_CREATION_ENABLED = False
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        response = client.post(reverse('adopts:api'), {
            'name': 'Foo',
            'short_name': 'foo',
        })

        self.assertEqual(response.status_code, 403)
        self.assertEqual(user.adopts.filter(
            name='Foo', short_name='foo').exists(), False)

    def test_creates_adopt(self):
        client = APIClient()

        user = UserFactory()
        client.force_login(user)

        response = client.post(reverse('adopts:api'), {
            'name': 'Foo',
            'short_name': 'foo',
        })

        self.assertEqual(response.status_code, 201)
        adopt = user.adopts.filter(name='Foo', short_name='foo').get()
        self.assertEqual(response.data, AdoptSerializer(adopt).data)


class AdoptApiUpdateTests(TestCase):

    def test_fails_when_not_authenticated(self):
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

    def test_fails_when_not_authenticated(self):
        client = APIClient()
        response = client.delete(reverse('adopts:api'))
        self.assertEqual(response.status_code, 403)

    def test_deletes_my_adopt(self):
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
