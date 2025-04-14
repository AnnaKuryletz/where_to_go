import os
import json
import requests

from urllib.parse import unquote, urlparse
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place, Image


def get_filename_from_url(url):
    url_part = urlparse(url).path
    unquoted_url_part = unquote(url_part)
    filename = os.path.split(unquoted_url_part)[-1]
    return filename


class Command(BaseCommand):
    help = 'Загружает место из JSON по ссылке'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL до JSON-файла')

    def handle(self, *args, **options):
        json_url = options['json_url']
        self.stdout.write(f'📦 Загрузка: {json_url}')

        response = requests.get(json_url)
        response.raise_for_status()
        place_json = response.json()

        place, created = Place.objects.get_or_create(
            title=place_json['title'],
            defaults={
                "description_short": place_json['description_short'],
                "description_long": place_json['description_long'],
                "lng": place_json['coordinates']['lng'],
                "lat": place_json['coordinates']['lat'],
            },
        )

        if created:
            self.stdout.write(f'✅ Место создано: {place.title}')
        else:
            self.stdout.write(f'ℹ️ Место уже существует: {place.title}')

        for img_url in place_json['imgs']:
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            image_content = ContentFile(img_response.content)
            img_name = get_filename_from_url(img_url)
            image = Image.objects.create(place=place)
            image.image.save(img_name, image_content, save=True)
            self.stdout.write(f'🖼 Загружено изображение: {img_name}')
