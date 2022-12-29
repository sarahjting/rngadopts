from colors import models
from django.utils import timezone
from django.conf import settings
import json


def create_color_pool_presets(adopt):
    file = open(settings.BASE_DIR / "colors/data/presets.json", "r")
    data = json.load(file)
    for color in data:
        create_color_pool(
            name=color['name'],
            colors="\n".join(color['colors']),
            adopt=adopt
        )


def create_color_pool(adopt, name, colors):
    color_pool = models.ColorPool(adopt=adopt, name=name, colors=colors)
    color_pool.save()

    adopt.colors_count += 1
    adopt.save()

    return color_pool


def delete_color_pool(color_pool):
    color_pool.date_deleted = timezone.now()
    color_pool.save()

    color_pool.adopt.colors_count -= 1
    color_pool.adopt.save()
