from genes import models
from django.utils import timezone
import random


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


def pick_genes_from_pool(gene_pool):
    all_genes = gene_pool.genes.all()
    if len(all_genes) == 0:
        return []

    selected_genes = []

    if gene_pool.type == "multi":
        for gene in all_genes:
            if random.randint(1, 100) <= gene.weight:
                selected_genes.append(gene)
    else:
        i = 0
        pool_weight = sum([x.weight for x in all_genes])
        offset = random.randint(1, pool_weight)
        while True:
            offset -= all_genes[i].weight
            if offset <= 0 or i >= len(all_genes):
                selected_genes.append(all_genes[i])
                break
            i += 1

    return selected_genes


def my_rand():
    return random.randint(1, 10)
