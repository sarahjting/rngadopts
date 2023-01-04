from django.test import TestCase
from adopts.adopt_gen import AdoptGenerator
from adopts.factories import AdoptFactory
from genes.factories import GeneFactory, GenePoolFactory, GeneLayerFactory
from colors.factories import ColorPoolFactory
import json


class AdoptGeneratorTest(TestCase):
    def setUp(self):
        self.adopt = AdoptFactory(short_name="Test")
        self.color_pool = ColorPoolFactory(adopt=self.adopt, colors="Buzz")
        self.gene_pools = [GenePoolFactory(adopt=self.adopt, color_pool=self.color_pool, name="A", type="multi"),
                           GenePoolFactory(adopt=self.adopt, color_pool=self.color_pool, name="B", type="multi")]

        self.gene_with_color = GeneFactory(
            gene_pool=self.gene_pools[0], name="Foo", weight=100)
        GeneLayerFactory(gene=self.gene_with_color, type="color_on")

        self.gene_with_required_gene = GeneFactory(
            gene_pool=self.gene_pools[0], name="Bar", weight=100)
        GeneLayerFactory(gene=self.gene_with_required_gene,
                         type="color_on", required_gene_id=self.gene_with_color.id, )

        self.gene_without_color = GeneFactory(
            gene_pool=self.gene_pools[1], name="Baz", weight=100)
        GeneLayerFactory(gene=self.gene_without_color, type="static_over")

    def test_randomizes(self):
        gen = AdoptGenerator(self.adopt)
        self.assertEqual(self.adopt, gen.adopt)
        self.assertEqual([], gen.gene_colors)

        gen.randomize()

        self.assertEqual(self.gene_with_required_gene,
                         gen.gene_colors[0]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[0]["color_pool"])
        self.assertEqual("Buzz", gen.gene_colors[0]["color"].name)

        # colorless genes still generate with a color, it just gets excluded in the data string
        self.assertEqual(self.gene_with_color, gen.gene_colors[1]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[1]["color_pool"])
        self.assertEqual("Buzz", gen.gene_colors[1]["color"].name)

        self.assertEqual(self.gene_without_color, gen.gene_colors[2]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[2]["color_pool"])
        self.assertEqual("Buzz", gen.gene_colors[2]["color"].name)

    def test_to_dict(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual({
            "adopt_id": self.adopt.id,
            "gene_colors": [
                {"gene": {"id": self.gene_with_required_gene.id, "name": self.gene_with_required_gene.name, "gene_pool_id": self.gene_pools[0].id},
                 "color": {"name": "Buzz", "slug": "buzz", "color_pool_id": self.color_pool.id}},
                {"gene": {"id": self.gene_with_color.id, "name": self.gene_with_color.name, "gene_pool_id": self.gene_pools[0].id},
                 "color": {"name": "Buzz", "slug": "buzz", "color_pool_id": self.color_pool.id}},
                {"gene": {"id": self.gene_without_color.id, "name": self.gene_without_color.name, "gene_pool_id": self.gene_pools[1].id},
                 "color": {"name": "Buzz", "slug": "buzz", "color_pool_id": self.color_pool.id}},
            ]
        }, gen.to_dict())

    def test_to_json(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual(json.dumps(gen.to_dict()), gen.to_json())

    def test_to_data_string(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual("test-a_bar-a_foo_buzz-b_baz", gen.to_data_string())

    def test_to_data_string_with_implicit_id(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual("test-1-a_bar-a_foo_buzz-b_baz",
                         gen.to_data_string(True))

    def test_to_data_string_with_explicit_id(self):
        gen = AdoptGenerator(self.adopt)
        gen.randomize()
        self.assertEqual("test-10-a_bar-a_foo_buzz-b_baz",
                         gen.to_data_string(10))

    def test_from_data_string(self):
        gen = AdoptGenerator(self.adopt)
        gen.from_data_string("a_foo_buzz-a_bar_buzz-b_baz_buzz")
        self.assertEqual(3, len(gen.gene_colors))
        self.assertEqual(self.gene_with_color,
                         gen.gene_colors[0]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[0]["color_pool"])
        self.assertEqual("Buzz", gen.gene_colors[0]["color"].name)
        self.assertEqual(self.gene_with_required_gene,
                         gen.gene_colors[1]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[1]["color_pool"])
        self.assertEqual("Buzz", gen.gene_colors[1]["color"].name)
        self.assertEqual(self.gene_without_color,
                         gen.gene_colors[2]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[2]["color_pool"])
        self.assertEqual("Buzz", gen.gene_colors[2]["color"].name)

        gen.from_data_string("a_foo-a_bar")
        self.assertEqual(2, len(gen.gene_colors))
        self.assertEqual(self.gene_with_color, gen.gene_colors[0]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[0]["color_pool"])
        self.assertEqual(None, gen.gene_colors[0]["color"])
        self.assertEqual(self.gene_with_required_gene,
                         gen.gene_colors[1]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[1]["color_pool"])
        self.assertEqual(None, gen.gene_colors[1]["color"])

        gen.from_data_string("a_foo_buzz")
        self.assertEqual(1, len(gen.gene_colors))
        self.assertEqual(self.gene_with_color, gen.gene_colors[0]["gene"])
        self.assertEqual(self.color_pool, gen.gene_colors[0]["color_pool"])
        self.assertEqual("Buzz", gen.gene_colors[0]["color"].name)
