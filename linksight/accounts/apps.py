from django.apps import AppConfig
from linksight.accounts.signals import record_survey
from registration.signals import user_registered


class AccountsConfig(AppConfig):
    name = 'linksight.accounts'

    def ready(self):
        user_registered.connect(record_survey)
