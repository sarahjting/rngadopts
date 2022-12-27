import factory
from .models import ColorPool
from adopts.factories import AdoptFactory


class ColorPoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ColorPool

    name = factory.Faker('word')
    adopt = factory.SubFactory(AdoptFactory)
    colors = [
        {
            'name': 'White',
            'palette': [
                {'base': '#ffffff', 'shading': '#ffffff', 'highlight': '#ffffff'}
            ],
        },
        {
            'name': 'Gray',
            'palette': [
                {'base': '#000000', 'shading': '#000000', 'highlight': '#000000'}
            ],
        },
        {
            'name': 'Black',
            'palette': [
                {'base': '#000000', 'shading': '#000000', 'highlight': '#000000'}
            ],
        },
    ]
