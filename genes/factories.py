from adopts.factories import AdoptFactory
from colors.factories import ColorPoolFactory
import factory
from .models import Gene, GeneLayer, GenePool
from django.utils.text import slugify


class GenePoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenePool

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    type = 'basic'
    adopt = factory.SubFactory(AdoptFactory)
    color_pool = factory.SubFactory(ColorPoolFactory)


class GeneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gene

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    gene_pool = factory.SubFactory(GenePoolFactory)
    adopt = factory.SubFactory(AdoptFactory)


class GeneLayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GeneLayer

    gene = factory.SubFactory(GeneFactory)
    adopt = factory.SubFactory(AdoptFactory)
