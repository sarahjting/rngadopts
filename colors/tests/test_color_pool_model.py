from colors.models import ColorPool
from django.test import TestCase


class ColorPoolModelTests(TestCase):
    def test_palette_count_with_one_color(self):
        color_pool = ColorPool(colors="foo #aaa #bbb #ccc")
        self.assertEqual(color_pool.palettes_count(), 1)
        self.assertEqual(color_pool.colors_count(), 1)

    def test_palette_count_with_multiple_colors(self):
        color_pool = ColorPool(
            colors="foo #aaa #bbb #ccc\nbar #aaa #bbb #ccc\nbaz #aaa #bbb #ccc")
        self.assertEqual(color_pool.palettes_count(), 1)
        self.assertEqual(color_pool.colors_count(), 3)

    def test_color_count_with_multiple_palettes(self):
        color_pool = ColorPool(
            colors="foo #aaa #bbb #ccc #aaa #bbb #ccc #aaa #bbb #ccc")
        self.assertEqual(color_pool.palettes_count(), 3)
        self.assertEqual(color_pool.colors_count(), 1)
