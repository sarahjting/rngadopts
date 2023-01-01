from adopts.factories import AdoptFactory
from adopts.serializers import AdoptSerializer, AdoptListSerializer
from django.conf import settings
from django.test import TestCase


class AdoptSerializerTests(TestCase):
    def test_serializes(self):
        adopt = AdoptFactory()
        self.assertEqual(AdoptSerializer(adopt).data, {
            'id': adopt.id,
            'name': adopt.name,
            'short_name': adopt.short_name,
            'logs_count': 0,
            'current_display_id': 1,
            'layers_count': 0,
            'colors_count': 0,
            'genes_count': 0,
            'width': 100,
            'height': 100,
            'date_updated': adopt.date_updated.strftime(settings.DATETIME_FORMAT),
            'adopt_layers': [],
            'gen_caption': '',
        })


class AdoptListSerializerTests(TestCase):
    def test_serializes(self):
        adopt = AdoptFactory()
        self.assertEqual(AdoptListSerializer(adopt).data, {
            'id': adopt.id,
            'name': adopt.name,
            'short_name': adopt.short_name,
            'logs_count': 0,
            'current_display_id': 1,
            'date_updated': adopt.date_updated.strftime(settings.DATETIME_FORMAT),
        })
