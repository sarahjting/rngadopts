from django.test import TestCase
from adopts.adopt_gen import AdoptGeneratorGenePicker
from unittest import mock
from adopts.factories import AdoptFactory
from genes.factories import GeneFactory, GenePoolFactory


class AdoptGeneratorGenePickerTests(TestCase):
    def test_picks_multiple_pools(self):
        adopt = AdoptFactory()
        gene_pools = [GenePoolFactory(
            adopt=adopt), GenePoolFactory(adopt=adopt)]
        genes = [GeneFactory(gene_pool=gene_pools[0], weight=1), GeneFactory(
            gene_pool=gene_pools[1], weight=1)]
        self.assertEqual(genes, AdoptGeneratorGenePicker(adopt).pick())

    def test_pick_genes_from_pool_picks_no_genes_when_empty(self):
        gene_pool = GenePoolFactory()
        self.assertEqual([], AdoptGeneratorGenePicker(
            gene_pool.adopt).pick_from_pool(gene_pool))

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
            [uncommon_gene_expected, common_gene_expected], AdoptGeneratorGenePicker(
                gene_pool.adopt).pick_from_pool(gene_pool))

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
            [expected_gene], AdoptGeneratorGenePicker(
                gene_pool.adopt).pick_from_pool(gene_pool))
