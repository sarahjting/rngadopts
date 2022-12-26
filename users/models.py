# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username

    def is_discord_verified(self):
        return hasattr(self, 'discord_user')


class DiscordUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.RESTRICT,
        related_name='discord_user'
    )
    discord_user_id = models.IntegerField(null=True, db_index=True)
    discord_user_username = models.CharField(max_length=32)
    discord_user_discriminator = models.CharField(max_length=4)
    discord_user_avatar = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.discord_user_username}#{self.discord_user_discriminator} ({self.discord_user_id})"
