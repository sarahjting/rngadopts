from django.apps import AppConfig
from allauth.account.signals import user_logged_in
from .actions import sync_social_account_data


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        user_logged_in.connect(sync_social_account_data)
