from colors.models import ColorPool, Color
from django.test import TestCase


class ColorPoolModelTests(TestCase):
    def test_get_color(self):
        color_pool = ColorPool(colors="foo #aaa #bbb #ccc\nbaz #aaa #bbb #ccc")
        self.assertEqual(
            color_pool.get_color(0).to_dict(),
            Color.from_db("foo #aaa #bbb #ccc")[0].to_dict()
        )
        self.assertEqual(
            color_pool.get_color(1).to_dict(),
            Color.from_db("baz #aaa #bbb #ccc")[0].to_dict()
        )
        self.assertEqual(color_pool.get_color(2), None)

    def test_get_palette(self):
        color_pool = ColorPool(
            colors="foo #aaa #bbb #ccc #ddd #eee #fff\nbaz #111 #222 #333 #444 #555 #666")
        self.assertEqual(
            color_pool.get_palette(0, 0).to_dict(),
            {"base": "#aaa", "shading": "#bbb", "highlight": "#ccc"}
        )
        self.assertEqual(
            color_pool.get_palette(0, 1).to_dict(),
            {"base": "#ddd", "shading": "#eee", "highlight": "#fff"}
        )
        self.assertEqual(
            color_pool.get_palette(1, 0).to_dict(),
            {"base": "#111", "shading": "#222", "highlight": "#333"}
        )
        self.assertEqual(
            color_pool.get_palette(1, 1).to_dict(),
            {"base": "#444", "shading": "#555", "highlight": "#666"}
        )
        self.assertEqual(color_pool.get_palette(1, 2), None)

    def test_get_hex(self):
        color_pool = ColorPool(
            colors="foo #aaa #bbb #ccc #ddd #eee #fff\nbaz #111 #222 #333 #444 #555 #666")
        self.assertEqual(color_pool.get_hex(0, 0, "base"), "#aaa")
        self.assertEqual(color_pool.get_hex(0, 0, "shading"), "#bbb")
        self.assertEqual(color_pool.get_hex(0, 0, "highlight"), "#ccc")
        self.assertEqual(color_pool.get_hex(1, 1, "base"), "#444")
        self.assertEqual(color_pool.get_hex(1, 1, "shading"), "#555")
        self.assertEqual(color_pool.get_hex(1, 1, "highlight"), "#666")
        self.assertEqual(color_pool.get_hex(0, 0, "foo"), None)

    def test_palette_count_with_one_color(self):
        color_pool = ColorPool(colors="foo #aaa #bbb #ccc")
        self.assertEqual(color_pool.palettes_count, 1)
        self.assertEqual(color_pool.colors_count, 1)

    def test_palette_count_with_multiple_colors(self):
        color_pool = ColorPool(
            colors="foo #aaa #bbb #ccc\nbar #aaa #bbb #ccc\nbaz #aaa #bbb #ccc")
        self.assertEqual(color_pool.palettes_count, 1)
        self.assertEqual(color_pool.colors_count, 3)

    def test_color_count_with_multiple_palettes(self):
        color_pool = ColorPool(
            colors="foo #aaa #bbb #ccc #aaa #bbb #ccc #aaa #bbb #ccc")
        self.assertEqual(color_pool.palettes_count, 3)
        self.assertEqual(color_pool.colors_count, 1)
