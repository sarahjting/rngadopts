from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from genes.actions import pick_genes_from_pool
from unittest import mock
from genes.factories import GeneFactory, GenePoolFactory


class TestPickGenesFromPool(TestCase):
    def test_pick_genes_from_pool_picks_no_genes_when_empty(self):
        gene_pool = GenePoolFactory()
        self.assertEqual([], pick_genes_from_pool(gene_pool))

    @mock.patch('random.randint')
    def test_pick_genes_from_pool_picks_multiple_genes(self, randomint_mock):
        randomint_mock.return_value = 25
        gene_pool = GenePoolFactory(type="multi")
        rare_gene_not_expected = GeneFactory(gene_pool=gene_pool, weight=1)
        uncommon_gene_not_expected = GeneFactory(
            gene_pool=gene_pool, weight=24)
        uncommon_gene_expected = GeneFactory(gene_pool=gene_pool, weight=25)
        common_gene_expected = GeneFactory(gene_pool=gene_pool, weight=75)
        self.assertEqual(
            [uncommon_gene_expected, common_gene_expected], pick_genes_from_pool(gene_pool))

    @mock.patch('random.randint')
    def test_pick_genes_from_pool_picks_basic_gene(self, randomint_mock):
        randomint_mock.return_value = 25
        gene_pool = GenePoolFactory(type="basic")
        GeneFactory(gene_pool=gene_pool, weight=1)
        expected_gene = GeneFactory(
            gene_pool=gene_pool, weight=24)
        GeneFactory(gene_pool=gene_pool, weight=25)
        GeneFactory(gene_pool=gene_pool, weight=75)
        self.assertEqual(
            [expected_gene], pick_genes_from_pool(gene_pool))
