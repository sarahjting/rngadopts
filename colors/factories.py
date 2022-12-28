import factory
from .models import ColorPool
from adopts.factories import AdoptFactory


class ColorPoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ColorPool

    name = factory.Faker('word')
    adopt = factory.SubFactory(AdoptFactory)
    colors = 'White #ffffff #ffffff #ffffff\nGray #000000 #000000 #000000\nBlack #000000 #000000 #000000'
