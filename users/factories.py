import factory
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user_%d' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
