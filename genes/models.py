from colors.models import ColorPool
from django.db import models
from os.path import splitext
from rngadopts import mixins


class GenePoolQuerySet(models.QuerySet, mixins.queryset.SoftDeletes):
    pass


class GenePool(models.Model):
    objects = GenePoolQuerySet.as_manager()

    adopt = models.ForeignKey(
        'adopts.Adopt', on_delete=models.RESTRICT, related_name='gene_pools')
    color_pool = models.ForeignKey(ColorPool, on_delete=models.RESTRICT)
    name = models.CharField(max_length=40)
    slug = models.CharField(max_length=40)
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


class GeneQuerySet(models.QuerySet, mixins.queryset.SoftDeletes):
    pass


class Gene(models.Model):
    objects = GeneQuerySet.as_manager()

    adopt = models.ForeignKey(
        'adopts.Adopt', on_delete=models.RESTRICT, related_name='genes')
    gene_pool = models.ForeignKey(
        GenePool, on_delete=models.RESTRICT, related_name='genes')
    name = models.CharField(max_length=40)
    slug = models.CharField(max_length=40)
    has_lines = models.BooleanField(default=False)
    has_color = models.BooleanField(default=True)
    color_pool = models.ForeignKey(
        ColorPool, null=True, on_delete=models.RESTRICT
    )
    weight = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    def get_has_color(self):
        return len([x for x in self.gene_layers.all() if x.type[0:6] == "color_" and x.required_gene_id is None and x.required_gene_pool_id is None]) > 0


def gene_layer_to_image_path(obj, filename):
    return f'adopts/{obj.adopt_id}/genes/{obj.gene_id}/{obj.id}{splitext(filename)[1]}'


class GeneLayer(models.Model):
    class Meta:
        ordering = ('-sort',)

    adopt = models.ForeignKey(
        'adopts.Adopt', on_delete=models.RESTRICT, related_name='gene_layers')
    gene = models.ForeignKey(
        Gene, on_delete=models.RESTRICT, related_name='gene_layers')
    image = models.ImageField(null=True, upload_to=gene_layer_to_image_path)
    type = models.CharField(
        max_length=20,
        choices=[
            ('static_over', 'Static on top of adopt'),
            ('shading_over', 'Shading on top of adopt'),
            ('highlights_over', 'Highlights on top of adopt'),
            ('color_over', 'Color pool on top of adopt'),
            ('static_on', 'Static on base'),
            ('color_on', 'Color on base'),
            ('static_under', 'Static under adopt'),
            ('shading_under', 'Shading under adopt'),
            ('highlights_under', 'Highlights under adopt'),
            ('color_under', 'Color under adopt'),
        ]
    )
    color_key = models.IntegerField(null=True)
    sort = models.IntegerField(default=0)
    required_gene_pool = models.ForeignKey(
        GenePool, on_delete=models.RESTRICT, related_name='dependent_gene_layers', null=True)
    required_gene = models.ForeignKey(
        Gene, on_delete=models.RESTRICT, related_name='dependent_gene_layers', null=True)
