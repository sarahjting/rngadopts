from adopts import models
from django.utils import timezone

from colors.actions import create_color_pool_presets


def create_adopt(name, short_name, mod=None):
    adopt = models.Adopt(name=name, short_name=short_name)
    adopt.save()

    if mod:
        adopt.mods.add(mod)

    create_color_pool_presets(adopt)
    return adopt


def delete_adopt(adopt):
    adopt.date_deleted = timezone.now()
    adopt.save()


def create_adopt_layer(adopt, type, image, gene_pool=None, sort=0):
    adopt_layer = models.AdoptLayer(adopt=adopt, type=type,
                                    image=image, gene_pool=gene_pool, sort=sort)
    adopt_layer.save()

    adopt.layers_count += 1
    adopt.save()

    return adopt_layer


def delete_adopt_layer(adopt_layer):
    adopt = adopt_layer.adopt
    adopt.layers_count -= 1
    adopt.save()

    adopt_layer.delete()
