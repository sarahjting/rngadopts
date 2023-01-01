from adopts import models
from django.utils import timezone

from colors.actions import create_color_pool_presets


def create_adopt(name, short_name, width, height, gen_caption, current_display_id=1, mod=None):
    adopt = models.Adopt(name=name, short_name=short_name,
                         width=width, height=height, gen_caption=gen_caption, current_display_id=1)
    adopt.save()

    if mod:
        adopt.mods.add(mod)

    create_color_pool_presets(adopt)
    return adopt


def create_adopt_logs_from_discord(social_account, adopt, gens, display_ids, discord_command_message, discord_response_message):
    for key in range(0, len(display_ids)):
        log = models.AdoptLog(
            adopt_id=adopt.id,
            mod_id=social_account.user_id,
            discord_user_id=discord_command_message.author.id,
            discord_guild_id=discord_command_message.guild.id,
            discord_channel_id=discord_command_message.channel.id,
            discord_message_id=discord_command_message.id,
            display_id=display_ids[key],
            image_code=discord_response_message.attachments[key].url.split(
                '/').pop().split('.')[0],
            image_url=discord_response_message.attachments[key].url,
            command=discord_command_message.content,
            result=gens[key].to_json())
        log.save()

    adopt.current_display_id = display_ids[-1] + 1
    adopt.save()


def delete_adopt(adopt):
    adopt.date_deleted = timezone.now()
    adopt.save()


def create_adopt_layer(adopt, type, image=None, gene_pool=None, sort=0):
    adopt_layer = models.AdoptLayer(adopt=adopt, type=type,
                                    image=image, gene_pool=gene_pool, sort=sort)
    adopt_layer.save()

    adopt.layers_count += 1
    adopt.save()

    return adopt_layer


def delete_adopt_layer(adopt_layer):
    adopt = adopt_layer.adopt
    adopt.layers_count -= 1
    adopt.save()

    adopt_layer.delete()
