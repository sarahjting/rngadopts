from genes import models
from django.utils import timezone


def create_gene_pool(adopt, name, type, color_pool):
    gene_pool = models.GenePool(
        adopt=adopt, name=name, type=type, color_pool=color_pool)
    gene_pool.save()

    adopt = gene_pool.adopt
    adopt.genes_count += 1
    adopt.save()

    return gene_pool


def delete_gene_pool(gene_pool):
    gene_pool.date_deleted = timezone.now()
    gene_pool.save()

    adopt = gene_pool.adopt
    adopt.genes_count -= 1
    adopt.save()


def create_gene(adopt, gene_pool, name, color_pool=None, weight=1):
    gene = models.Gene(adopt=adopt, gene_pool=gene_pool,
                       name=name, color_pool=color_pool, weight=weight)
    gene.save()

    gene_pool.genes_count += 1
    gene_pool.genes_weight_total += weight
    gene_pool.save()

    return gene


def update_gene(gene, **kwargs):

    weight_delta = 0
    if 'name' in kwargs:
        gene.name = kwargs['name']
    if 'color_pool' in kwargs:
        gene.color_pool = kwargs['color_pool']
    if 'weight' in kwargs:
        if gene.weight != kwargs['weight']:
            weight_delta = kwargs['weight'] - gene.weight
        gene.weight = kwargs['weight']
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

    gene.date_deleted = timezone.now()
    gene.save()


def create_gene_layer(adopt, gene, image, type, color_key=None, sort=0):
    gene_layer = models.GeneLayer(
        adopt=adopt, gene=gene, image=image, type=type, color_key=color_key, sort=sort)
    gene_layer.save()
    return gene_layer
