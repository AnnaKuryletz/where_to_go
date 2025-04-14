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


def load_place_from_data(place_json):
    place, created = Place.objects.get_or_create(
        title=place_json['title'],
        defaults={
            "short_description": place_json['short_description'],
            "description_long": place_json['description_long'],
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


def load_places_from_folder(folder):
    json_files_paths = [
        os.path.join(folder, filename) for filename in os.listdir(folder)
        if filename.endswith(".json")
    ]

    for path in json_files_paths:
        with open(Path(path), 'r', encoding='utf-8') as json_file:
            place_json = json.load(json_file)
        load_place_from_data(place_json)


def load_place_from_url(url):
    print(f"📦 Загрузка: {url}")
    response = requests.get(url)
    response.raise_for_status()
    place_json = response.json()
    load_place_from_data(place_json)


class Command(BaseCommand):
    help = 'Загружает места из JSON-файлов (папка или URL)'

    def add_arguments(self, parser):
        parser.add_argument('-j', '--json_folder', help='Путь к папке с JSON-файлами')
        parser.add_argument('-u', '--json_url', help='URL JSON-файла для загрузки')

    def handle(self, *args, **options):
        json_folder = options.get('json_folder')
        json_url = options.get('json_url')

        if json_url:
            load_place_from_url(json_url)
        elif json_folder:
            load_places_from_folder(json_folder)
        else:
            self.stderr.write(self.style.ERROR(
                'Укажи либо --json_folder, либо --json_url для загрузки.'))
