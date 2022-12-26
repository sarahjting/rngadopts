from django.urls import reverse
from django.test import TestCase

from users.models import DiscordUser, User


class UserMeViewTests(TestCase):

    def test_not_logged_in(self):
        response = self.client.get(reverse('users:me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

    def test_logged_in(self):
        user = User.objects.create()
        self.client.force_login(user)
        response = self.client.get(reverse('users:me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': user.id,
            'username': user.username,
            'is_discord_verified': False,
        })


class UserModelTests(TestCase):

    def test_is_discord_verified_returns_false_when_not_discord_verified(self):
        user = User()
        self.assertIs(user.is_discord_verified(), False)

    def test_is_discord_verified_returns_true_when_discord_verified(self):
        user = User()
        user.save()

        discord_user = DiscordUser(
            user=user,
            discord_user_id=12345678,
            discord_user_username='foo',
            discord_user_discriminator='1234',
            discord_user_avatar='https://discord.com/fakeurl.png'
        )

        discord_user.save()

        self.assertIs(user.is_discord_verified(), True)
