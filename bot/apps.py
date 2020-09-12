from django.apps import AppConfig
from django.conf import settings


class BotConfig(AppConfig):
    name = 'bot'

    def ready(self):
        from .models import Language

        for lang in Language.objects.all():
            settings.AVAILABLE_LANGUAGES.append(lang.name)