from django.urls import reverse
from django.test import TestCase
from users.factories import UserFactory, UserVerifiedFactory

from users.serializers import UserSerializer


class UserApiMeViewTests(TestCase):

    def test_not_logged_in(self):
        response = self.client.get(reverse('users:me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

    def test_logged_in(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('users:me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UserSerializer(user).data)


class UserSerializerTests(TestCase):
    def test_serializer(self):
        user = UserFactory()
        self.assertEqual(UserSerializer(user).data, {
            'id': user.id,
            'username': user.username,
            'is_discord_verified': False,
        })


class UserModelTests(TestCase):

    def test_is_discord_verified_returns_false_when_not_discord_verified(self):
        user = UserFactory()
        self.assertIs(user.is_discord_verified(), False)

    def test_is_discord_verified_returns_true_when_discord_verified(self):
        user = UserVerifiedFactory()
        self.assertIs(user.is_discord_verified(), True)
