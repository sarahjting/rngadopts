from django.db import models
from users.models import User


class Adopt(models.Model):
    name = models.CharField(max_length=40)
    short_name = models.CharField(max_length=20, unique=True)
    count = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)
    mods = models.ManyToManyField(
        User, through='AdoptMod', related_name='adopts'
    )

    def __str__(self):
        return f"{self.name} ({self.short_name})"


class AdoptLog(models.Model):
    adopt = models.ForeignKey(Adopt, on_delete=models.RESTRICT)
    mod = models.ForeignKey(User, on_delete=models.RESTRICT)
    discord_user_id = models.IntegerField(null=True, db_index=True)
    discord_guild_id = models.IntegerField(null=True, db_index=True)
    discord_channel_id = models.IntegerField(null=True, db_index=True)
    discord_message_id = models.IntegerField(null=True, db_index=True)
    image_url = models.CharField(max_length=120)
    command = models.TextField()  # command that triggered the generation
    result = models.JSONField()  # stores the raw result of the generation

    def __str__(self):
        return f"Adopt Log #{self.id}"


class AdoptMod(models.Model):
    # django can make the pivot model implicitly, but doing it this way lets us add extra columns like date_promoted or rank
    adopt = models.ForeignKey(
        Adopt, db_column='adopt_id', on_delete=models.RESTRICT
    )
    mod = models.ForeignKey(
        User, db_column='mod_id', on_delete=models.RESTRICT
    )
    date_promoted = models.DateTimeField(auto_now_add=True)
