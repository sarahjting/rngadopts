from adopts.factories import AdoptFactory
from adopts.models import Adopt
from adopts.serializers import AdoptSerializer, AdoptListSerializer
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from users.factories import UserFactory


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
            'width': 100,
            'height': 100,
            'gen_caption': '',
            'current_display_id': 1,
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
    def _put(self, adopt, user=None, data={}):
        client = APIClient()

        if user:
            client.force_login(user)

        return client.put(reverse('adopts:api', kwargs={'pk': adopt.id}), {
            'name': 'Foo',
            'short_name': 'foo',
            'width': 101,
            'height': 101,
            'gen_caption': '',
            'current_display_id': 1,
        } | data)

    def test_fails_when_unauthenticated(self):
        adopt = AdoptFactory()
        response = self._put(adopt)
        self.assertEqual(response.status_code, 403)

    def test_updates_my_adopt(self):
        user = UserFactory()
        adopt = AdoptFactory(mods=(user,))

        response = self._put(adopt, user)

        self.assertEqual(response.status_code, 200)

        adopt = user.adopts.filter(
            id=adopt.id, name='Foo', short_name='foo', width=101, height=101).get()
        self.assertEqual(response.data, AdoptSerializer(adopt).data)

    def test_does_not_update_other_adopts(self):
        user = UserFactory()
        unrelated_user = UserFactory()
        unrelated_adopt = AdoptFactory(mods=(unrelated_user,))

        response = self._put(unrelated_adopt, user)

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

        self.assertEqual(response.status_code, 204)
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
