import factory
from . import models
from django.utils.text import slugify


class AdoptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Adopt

    name = factory.Sequence(lambda n: 'Adopt %d' % n)
    short_name = factory.LazyAttribute(lambda o: slugify(o.name))
    width = 100
    height = 100

    @factory.post_generation
    def mods(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.mods.add(user)


class AdoptLayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdoptLayer
