import os
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Loads a place from a JSON URL'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL to the JSON file')

    def handle(self, *args, **options):
        json_url = options['json_url']
        self.stdout.write(f'Fetching JSON from {json_url}...')

        response = requests.get(json_url)
        response.raise_for_status()
        place_json = response.json()

        place, created = Place.objects.get_or_create(
            title=place_json['title'],
            defaults={
                'description_short': place_json.get('description_short', ''),
                'description_long': place_json.get('description_long', ''),
                'coordinates_lng': place_json['coordinates']['lng'],
                'coordinates_lat': place_json['coordinates']['lat'],
            }
        )

        if not created:
            self.stdout.write(self.style.WARNING(f"Place '{place.title}' already exists. Skipping."))
            return

        for img_url in place_json.get('imgs', []):
            img_response = requests.get(img_url)
            img_response.raise_for_status()

            filename = os.path.basename(unquote(urlparse(img_url).path))
            image = Image(place=place)
            image.image.save(filename, ContentFile(img_response.content), save=True)

        self.stdout.write(self.style.SUCCESS(f"Place '{place.title}' successfully loaded."))
