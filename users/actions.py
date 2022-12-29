def sync_social_account_data(request, user, **kwargs):
    discord_account = user.get_discord_account()
    user.avatar_url = 'https://cdn.discordapp.com/avatars/{}/{}.jpg'.format(
        discord_account.uid, discord_account.extra_data['avatar'])
    user.save()
