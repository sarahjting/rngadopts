from adopts.factories import AdoptFactory
from colors.factories import ColorPoolFactory
import factory
from .models import Gene, GeneLayer, GenePool


class GenePoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenePool

    name = factory.Faker('word')
    type = 'basic'
    adopt = factory.SubFactory(AdoptFactory)
    color_pool = factory.SubFactory(ColorPoolFactory)


class GeneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gene

    name = factory.Faker('word')
    gene_pool = factory.SubFactory(GenePoolFactory)
    adopt = factory.SubFactory(AdoptFactory)


class GeneLayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GeneLayer

    gene = factory.SubFactory(GeneFactory)
    adopt = factory.SubFactory(AdoptFactory)
