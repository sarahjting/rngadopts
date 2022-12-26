from django.test import TestCase

from users.models import DiscordUser, User


class UserModelTest(TestCase):

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
