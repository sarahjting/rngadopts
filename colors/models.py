from django.db import models
from adopts.models import Adopt


class ColorPool(models.Model):
    adopt = models.ForeignKey(
        Adopt, on_delete=models.RESTRICT, related_name='color_pools')
    name = models.CharField(max_length=40)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)
    colors = models.JSONField(default=list)

    def __str__(self):
        return self.name
