from colors.models import ColorPool
from django.db import models
from os.path import splitext
from users.models import User
from rngadopts import mixins


class AdoptQuerySet(models.QuerySet, mixins.queryset.SoftDeletes):
    pass


class Adopt(models.Model):
    objects = AdoptQuerySet.as_manager()

    name = models.CharField(max_length=40)
    short_name = models.CharField(max_length=20, unique=True)
    logs_count = models.IntegerField(default=0)
    layers_count = models.IntegerField(default=0)
    colors_count = models.IntegerField(default=0)
    genes_count = models.IntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)
    mods = models.ManyToManyField(
        User, through='AdoptMod', related_name='adopts'
    )

    def __str__(self):
        return f"{self.name} ({self.short_name})"


def adopt_layer_to_image_path(obj, filename):
    return f'adopts/{obj.adopt_id}/layers/{obj.id}{splitext(filename)[1]}'


class AdoptLayer(models.Model):
    adopt = models.ForeignKey(
        Adopt, on_delete=models.RESTRICT, related_name='adopt_layers')
    image = models.ImageField(null=True, upload_to=adopt_layer_to_image_path)
    type = models.CharField(
        max_length=20,
        choices=[('static', 'Static image (eg. lines, eye whites)'), ('shading', 'Shading'),
                 ('highlights', 'Highlights'), ('color', 'Generate all colors from color pool (eg. eye color)')]
    )
    color_pool = models.ForeignKey(
        ColorPool, on_delete=models.RESTRICT, null=True)
    sort = models.IntegerField(default=0)


class AdoptLog(models.Model):
    adopt = models.ForeignKey(
        Adopt, on_delete=models.RESTRICT, related_name='adopt_logs')
    mod = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='adopt_logs')
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
