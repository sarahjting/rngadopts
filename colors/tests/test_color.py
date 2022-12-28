from colors.models import Color, ColorPalette
from django.test import TestCase


class ColorFromDbTests(TestCase):
    def test_fails_with_no_input(self):
        with self.assertRaises(AssertionError) as context:
            Color.from_db('')

    def test_fails_with_no_name(self):
        with self.assertRaises(AssertionError) as context:
            Color.from_db('#ccc #000 #fff')

    def test_builds_single_color(self):
        colors = Color.from_db('color1 #ccc #000 #fff')
        self.assertEqual(1, len(colors))
        self.assertIsInstance(colors[0], Color)
        self.assertEqual('color1', colors[0].name)
        self.assertIsInstance(colors[0].palettes, list)
        self.assertIsInstance(colors[0].palettes[0], ColorPalette)
        self.assertEqual('#ccc', colors[0].palettes[0].base)
        self.assertEqual('#000', colors[0].palettes[0].shading)
        self.assertEqual('#fff', colors[0].palettes[0].highlight)

    def test_builds_multiple_palettes(self):
        colors = Color.from_db('color1 #aaa #aab #aac #aba #abb #abc')
        self.assertEqual(1, len(colors))
        self.assertEqual('color1', colors[0].name)
        self.assertEqual(('#aaa', '#aab', '#aac'), (
            colors[0].palettes[0].base, colors[0].palettes[0].shading, colors[0].palettes[0].highlight))
        self.assertEqual(('#aba', '#abb', '#abc'), (
            colors[0].palettes[1].base, colors[0].palettes[1].shading, colors[0].palettes[1].highlight))

    def test_builds_multiple_colors(self):
        colors = Color.from_db(
            'color1 #aaa #aab #aac #aba #abb #abc\ncolor2 #baa #bab #bac #bba #bbb #bbc\ncolor3 #ca1 #cb1 #cc1 #ca1 #cb2 #cc3')
        self.assertEqual(3, len(colors))
        self.assertEqual('color1', colors[0].name)
        self.assertEqual(2, len(colors[0].palettes))
        self.assertEqual('color2', colors[1].name)
        self.assertEqual(2, len(colors[1].palettes))
        self.assertEqual('color3', colors[2].name)
        self.assertEqual(2, len(colors[2].palettes))
