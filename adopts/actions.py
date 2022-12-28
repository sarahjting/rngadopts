from adopts import models
from django.utils import timezone


def create_adopt(name, short_name, mod=None):
    adopt = models.Adopt(name=name, short_name=short_name)
    adopt.save()

    if mod:
        adopt.mods.add(mod)

    return adopt


def delete_adopt(adopt):
    adopt.date_deleted = timezone.now()
    adopt.save()


def create_adopt_layer(adopt, type, image, color_pool=None, sort=0):
    adopt_layer = models.AdoptLayer(adopt=adopt, type=type,
                                    image=image, color_pool=color_pool, sort=sort)
    adopt_layer.save()

    adopt.layers_count += 1
    adopt.save()

    return adopt_layer


def delete_adopt_layer(adopt_layer):
    adopt = adopt_layer.adopt
    adopt.layers_count -= 1
    adopt.save()

    adopt_layer.delete()