from colors.factories import ColorPoolFactory
from colors.serializers import ColorPoolSerializer
from django.conf import settings
from django.test import TestCase


class ColorPoolSerializerTests(TestCase):
    def test_serializes(self):
        color_pool = ColorPoolFactory()
        self.assertEqual(ColorPoolSerializer(color_pool).data, {
            'id': color_pool.id,
            'name': color_pool.name,
            'date_updated': color_pool.date_updated.strftime(settings.DATETIME_FORMAT),
            'colors': color_pool.colors,
            'colors_json': color_pool.colors_json(),
        })
