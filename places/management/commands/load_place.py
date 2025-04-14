import os
import json
import requests
import uuid

from pathlib import Path
from urllib.parse import unquote, urlparse

from places.models import Place, Image
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand


def get_filename_from_url(url):
    url_part = urlparse(url).path
    unquoted_url_part = unquote(url_part)
    filename = os.path.split(unquoted_url_part)[-1]
    return filename


def load_places(folder):
    json_files_paths = [
        os.path.join(folder, filename) for filename in os.listdir(folder)
        if filename.endswith(".json")
    ]

    for path in json_files_paths:
        with open(Path(path), 'r', encoding='utf-8') as json_file:
            place_json = json.load(json_file)

        place, created = Place.objects.get_or_create(
            title=place_json['title'],
            defaults={
                "short_description": place_json['description_short'],
                "long_description": place_json['description_long'],
                "lng": place_json['coordinates']['lng'],
                "lat": place_json['coordinates']['lat'],
                "placeId": str(uuid.uuid4()),
            },
        )

        if created:
            print(f"✅ Место создано: {place.title}")
        else:
            print(f"🔁 Место уже существует: {place.title}")

        for img_url in place_json['imgs']:
            response = requests.get(img_url)
            response.raise_for_status()
            content = ContentFile(response.content)
            img_name = get_filename_from_url(img_url)
            image_object = Image.objects.create(place=place)
            image_object.image.save(name=img_name, content=content, save=True)
            print(f"🖼 Загружено изображение: {img_name}")


class Command(BaseCommand):

    help = 'Загружает места из JSON-файлов в указанной папке'

    def add_arguments(self, parser):
        parser.add_argument(
            '-j',
            '--json_folder',
            required=True,
            help='Путь к папке с JSON-файлами'
        )

    def handle(self, *args, **options):
        load_places(options['json_folder'])
