import factory
from . import models
from django.utils.text import slugify


class AdoptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Adopt

    name = factory.Faker('word')
    short_name = factory.LazyAttribute(lambda o: slugify(o.name))

    @factory.post_generation
    def mods(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.mods.add(user)
