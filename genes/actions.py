from genes import models
from django.utils import timezone
import random


def create_gene_pool(adopt, name, slug, type, color_pool):
    gene_pool = models.GenePool(
        adopt=adopt, name=name, slug=slug, type=type, color_pool=color_pool)
    gene_pool.save()

    adopt = gene_pool.adopt
    adopt.genes_count += 1
    adopt.save()

    return gene_pool


def delete_gene_pool(gene_pool):
    gene_pool.date_deleted = timezone.now()
    gene_pool.slug = ""
    gene_pool.save()

    adopt = gene_pool.adopt
    adopt.genes_count -= 1
    adopt.save()


def create_gene(adopt, gene_pool, name, slug, color_pool=None, weight=1, has_color=True):
    gene = models.Gene(adopt=adopt, gene_pool=gene_pool, name=name, slug=slug,
                       color_pool=color_pool, weight=weight, has_color=has_color)
    gene.save()

    gene_pool.genes_count += 1
    gene_pool.genes_weight_total += weight
    gene_pool.save()

    return gene


def update_gene(gene, **kwargs):
    weight_delta = 0
    if 'name' in kwargs:
        gene.name = kwargs['name']
    if 'slug' in kwargs:
        gene.slug = kwargs['slug']
    if 'color_pool' in kwargs:
        gene.color_pool = kwargs['color_pool']
    if 'weight' in kwargs:
        if gene.weight != kwargs['weight']:
            weight_delta = kwargs['weight'] - gene.weight
        gene.weight = kwargs['weight']
    if 'has_color' in kwargs:
        gene.has_color = kwargs['has_color']
    gene.save()

    if weight_delta != 0:
        gene_pool = gene.gene_pool
        gene_pool.genes_weight_total += weight_delta
        gene_pool.save()

    return gene


def delete_gene(gene):
    gene_pool = gene.gene_pool
    gene_pool.genes_count -= 1
    gene_pool.genes_weight_total -= gene.weight
    gene_pool.save()

    gene.slug = ""
    gene.date_deleted = timezone.now()
    gene.save()


def create_gene_layer(adopt, gene, image, type, required_gene=None, required_gene_pool=None, color_key=None, sort=0):
    gene_layer = models.GeneLayer(
        adopt=adopt, gene=gene, image=image, type=type, color_key=color_key, sort=sort, required_gene=required_gene, required_gene_pool=required_gene_pool)
    gene_layer.save()
    return gene_layer


def my_rand():
    return random.randint(1, 10)
