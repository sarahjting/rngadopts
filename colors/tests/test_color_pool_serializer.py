from adopts.serializers import AdoptListSerializer
from colors.factories import ColorPoolFactory
from colors.serializers import ColorPoolSerializer, ColorPoolListSerializer
from django.conf import settings
from django.test import TestCase


class ColorPoolListSerializerTests(TestCase):
    def test_serializes(self):
        color_pool = ColorPoolFactory()
        self.assertEqual(ColorPoolListSerializer(color_pool).data, {
            'id': color_pool.id,
            'name': color_pool.name,
            'date_updated': color_pool.date_updated.strftime(settings.DATETIME_FORMAT),
            'colors_count': color_pool.colors_count(),
            'palettes_count': color_pool.palettes_count(),
        })


class ColorPoolSerializerTests(TestCase):
    def test_serializes(self):
        color_pool = ColorPoolFactory()
        self.assertEqual(ColorPoolSerializer(color_pool).data, {
            'id': color_pool.id,
            'name': color_pool.name,
            'date_updated': color_pool.date_updated.strftime(settings.DATETIME_FORMAT),
            'colors': color_pool.colors,
            'colors_dict': color_pool.colors_dict(),
            'adopt': AdoptListSerializer(color_pool.adopt).data
        })
