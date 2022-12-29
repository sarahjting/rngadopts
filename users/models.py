from django.contrib.auth.models import AbstractUser
from django.db import models
from allauth.socialaccount.models import SocialAccount


class User(AbstractUser):
    avatar_url = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    def get_discord_account(self):
        return SocialAccount.objects.get(provider='discord', user_id=self.id)
