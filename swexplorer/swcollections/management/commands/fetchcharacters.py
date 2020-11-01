from django.core.management.base import BaseCommand
from swcollections.models import fetch_characters


class Command(BaseCommand):
    help = 'Fetches the Star Wars characters from SWAPI'

    def handle(self, *args, **kwargs):
        fetch_characters()
