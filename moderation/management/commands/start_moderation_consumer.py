from django.core.management import BaseCommand

from moderation.moderation_consumer import start_moderation_panel_consumer


class Command(BaseCommand):
    def handle(self, *args, **options):
        start_moderation_panel_consumer()
