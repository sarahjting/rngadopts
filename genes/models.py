from django.db import models

from adopts.models import Adopt
from colors.models import ColorPool


class GenePool(models.Model):
    adopt = models.ForeignKey(
        Adopt, on_delete=models.RESTRICT, related_name='gene_pools')
    color_pool = models.ForeignKey(ColorPool, on_delete=models.RESTRICT)
    name = models.CharField(max_length=40)
    type = models.CharField(
        max_length=10,
        choices=[('basic', 'Basic'), ('multi', 'Multi')]
    )
    genes_count = models.IntegerField(default=0)  # denormalize
    genes_weight_total = models.IntegerField(default=0)  # denormalize
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)
    sort = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Gene(models.Model):
    gene_pool = models.ForeignKey(
        GenePool, on_delete=models.RESTRICT, related_name='genes')
    name = models.CharField(max_length=40)
    has_lines = models.BooleanField(default=False)
    color_pool = models.ForeignKey(
        ColorPool, null=True, on_delete=models.RESTRICT
    )
    weight = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)

    def __str__(self):
        return self.name
