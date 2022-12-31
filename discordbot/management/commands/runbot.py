from django.core.management.base import BaseCommand, CommandError
from adopts.adopt_gen import AdoptGenerator, AdoptGeneratorImage
from django.conf import settings
from adopts.models import Adopt, AdoptMod
from allauth.socialaccount.models import SocialAccount
from asgiref.sync import sync_to_async
import discord
import io


class Command(BaseCommand):
    help = 'Runs the Discord bot'

    def handle(self, *args, **options):

        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f'We have logged in as {client.user}')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            command = message.content.split(" ")
            if command[0] == "$rngadopt":
                print(message.content, command)
                try:
                    adopt = await get_adopt(command[1])
                    social_account = await get_social_account(message.author.id)
                    await check_user_is_mod(adopt, social_account)

                    gen = await build_gen(adopt)
                    image = await build_image(gen)

                    with io.BytesIO() as image_binary:
                        image.to_pil().save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await message.channel.send(file=discord.File(fp=image_binary, filename=f"{gen.to_data_string()}.png"))
                        await message.channel.send(gen.__str__())
                except Adopt.DoesNotExist:
                    await message.channel.send(
                        "I couldn't find the adopt, please check that you are using the __short name__.")
                except (SocialAccount.DoesNotExist, AdoptMod.DoesNotExist):
                    await message.channel.send("That adopt doesn't belong to you.")

        @sync_to_async
        def get_adopt(short_name):
            return Adopt.objects.get(short_name=short_name)

        @sync_to_async
        def get_social_account(discord_user_id):
            return SocialAccount.objects.get(
                provider='discord', uid=discord_user_id)

        @sync_to_async
        def check_user_is_mod(adopt, social_account):
            AdoptMod.objects.get(
                adopt_id=adopt.id, mod_id=social_account.user_id)

        @sync_to_async
        def build_gen(adopt):
            return AdoptGenerator(adopt).randomize()

        @sync_to_async
        def build_image(gen):
            return AdoptGeneratorImage(gen)

        client.run(settings.DISCORDBOT_TOKEN)
