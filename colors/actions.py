from adopts import models
from django.utils import timezone


def create_color_pool(adopt, name, colors):
    color_pool = models.ColorPool(adopt=adopt, name=name, colors=colors)
    color_pool.save()
    return color_pool


def delete_color_pool(color_pool):
    color_pool.date_deleted = timezone.now()
    color_pool.save()