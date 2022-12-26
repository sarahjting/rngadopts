import factory
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user_%d' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)


class DiscordUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DiscordUser

    user = factory.SubFactory(UserFactory)
    discord_user_id = factory.Sequence(lambda n: n)
    discord_user_username = factory.LazyAttribute(
        lambda o: 'Discord User %d' % o.discord_user_id
    )
    discord_user_discriminator = factory.LazyAttribute(
        lambda o: '%04d' % o.discord_user_id
    )
    discord_user_avatar = factory.LazyAttribute(
        lambda o: 'https://discord.com/%d.png' % o.discord_user_id
    )


class UserVerifiedFactory(UserFactory):
    discord_user = factory.RelatedFactory(
        DiscordUserFactory,
        factory_related_name='user'
    )
