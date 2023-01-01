from django.core.management.base import BaseCommand, CommandError
from adopts.actions import create_adopt_logs_from_discord
from adopts.adopt_gen import AdoptGenerator, AdoptGeneratorImage
from django.conf import settings
from adopts.models import Adopt, AdoptMod
from allauth.socialaccount.models import SocialAccount
from asgiref.sync import sync_to_async
from collections import deque
import discord
import io


class Command(BaseCommand):
    help = 'Runs the Discord bot'

    def handle(self, *args, **options):
        PREFIX = "$rngadopt"
        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f'We have logged in as {client.user}')

        @client.event
        async def on_message(msg):
            if msg.author == client.user:
                return

            if msg.content == PREFIX:
                await msg.channel.send("Command should resemble: `$rngadopt {adopt_short_name} {number_to_generate} {extra_message}`\n EG: `$rngadopt raccoon 5 for @username`")
                return

            if msg.content[:(len(PREFIX) + 1)] != PREFIX + " ":
                return

            command = deque(msg.content.split(" "))
            command.popleft()

            try:
                # check adopt exists & user has permission
                adopt = await get_adopt(command.popleft())
                social_account = await get_social_account(msg.author.id)
                await check_user_is_mod(adopt, social_account)

                # number of adopts to generate (defaults to 0)
                if len(command) and command[0].isnumeric():
                    num = min(10, max(1, int(command.popleft())))
                else:
                    num = 1

                files = []
                gens = []
                display_ids = [adopt.current_display_id +
                               x for x in range(0, num)]

                # generate the adopts
                for display_id in display_ids:
                    gen = await build_gen(adopt)
                    image = await build_image(gen)
                    gens.append(gen)
                    with io.BytesIO() as image_binary:
                        image.to_pil().save(image_binary, 'PNG')
                        image_binary.seek(0)
                        files.append(discord.File(
                            fp=image_binary, filename=f"{gen.to_data_string(display_id)}.png"))

                # send the message with attachments
                response_msg = await msg.channel.send(files=files)

                # reformat any pings into plain usernames -- we don't want pings, this is going into a codeblock
                prefix = " ".join(command)
                for user in msg.mentions:
                    prefix = prefix.replace(
                        f"<@{user.id}>", f"@{user.name}")

                # send response message
                gen_caption = build_gen_caption(adopt, response_msg, prefix)
                if gen_caption:
                    await msg.channel.send(gen_caption)

                # finally log
                await log_gen(
                    social_account=social_account,
                    adopt=adopt,
                    gens=gens,
                    display_ids=display_ids,
                    discord_command_message=msg,
                    discord_response_message=response_msg,
                )
            except Adopt.DoesNotExist:
                await msg.channel.send(
                    "I couldn't find the adopt, please check that you are using the __short name__.")
            except (SocialAccount.DoesNotExist, AdoptMod.DoesNotExist):
                await msg.channel.send("That adopt doesn't belong to you.")

        def build_gen_caption(adopt, discord_response_message, extra_content=""):
            template = (extra_content + " " + adopt.gen_caption).strip()
            if template.replace(" ", "") == "":
                return None

            str = template.replace('[img]', ''.join([
                f"[img]{a.url}[/img]" for a in discord_response_message.attachments
            ]))

            return f"```{str}```"

        @sync_to_async
        def log_gen(**kwargs):
            create_adopt_logs_from_discord(**kwargs)

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
