from django.test import TestCase
from adopts.adopt_gen import AdoptGenerator
from adopts.factories import AdoptFactory
from genes.factories import GeneFactory, GenePoolFactory
from colors.factories import ColorPoolFactory
import json


class AdoptGeneratorTest(TestCase):
    def setUp(self):
        self.adopt = AdoptFactory()
        self.color_pool = ColorPoolFactory(adopt=self.adopt, colors="Baz")
        self.gene_pools = [GenePoolFactory(adopt=self.adopt, color_pool=self.color_pool, name="A"),
                           GenePoolFactory(adopt=self.adopt, color_pool=self.color_pool, name="B")]
        self.genes = [GeneFactory(gene_pool=self.gene_pools[0], name="Foo"),
                      GeneFactory(gene_pool=self.gene_pools[1], name="Bar")]

    def test_randomizes(self):
        gen = AdoptGenerator(self.adopt)
        self.assertEqual(self.adopt, gen.adopt)
        self.assertEqual([], gen.gene_colors)

        gen.randomize()
        self.assertEqual(self.genes[0], gen.gene_colors[0]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[0]["color_pool"])
        self.assertEqual("Baz", gen.gene_colors[0]["color"].name)
        self.assertEqual(self.genes[1], gen.gene_colors[1]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[1]["color_pool"])
        self.assertEqual("Baz", gen.gene_colors[1]["color"].name)

    def test_to_dict(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual({
            "adopt_id": self.adopt.id,
            "gene_colors": [
                {"gene": "Foo", "color": "Baz"},
                {"gene": "Bar", "color": "Baz"},
            ]
        }, gen.to_dict())

    def test_to_json(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual(json.dumps({
            "adopt_id": self.adopt.id,
            "gene_colors": [
                {"gene": "Foo", "color": "Baz"},
                {"gene": "Bar", "color": "Baz"},
            ]
        }), gen.to_json())

    def test_to_data_string(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual("a_foo_baz-b_bar_baz", gen.to_data_string())

    def test_from_data_string(self):
        gen = AdoptGenerator(self.adopt)
        gen.from_data_string("a_foo_baz-b_bar_baz")
        self.assertEqual(2, len(gen.gene_colors))
        self.assertEqual(self.genes[0], gen.gene_colors[0]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[0]["color_pool"])
        self.assertEqual("Baz", gen.gene_colors[0]["color"].name)
        self.assertEqual(self.genes[1], gen.gene_colors[1]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[1]["color_pool"])
        self.assertEqual("Baz", gen.gene_colors[1]["color"].name)

        gen.from_data_string("a_foo_baz")
        self.assertEqual(1, len(gen.gene_colors))
        self.assertEqual(self.genes[0], gen.gene_colors[0]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[0]["color_pool"])
        self.assertEqual("Baz", gen.gene_colors[0]["color"].name)