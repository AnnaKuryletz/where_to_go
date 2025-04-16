import json
import os
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Image, Place

def get_filename_from_url(url):
    url_part = urlparse(url).path
    unquoted_url_part = unquote(url_part)
    filename = os.path.split(unquoted_url_part)[-1]
    return filename


def load_place_from_data(raw_place):
    place, created = Place.objects.get_or_create(
        title=raw_place['title'],
        defaults={
            "description_short": raw_place['short_description'],
            "description_long": raw_place['long_description'],
            "lng": raw_place['coordinates']['lng'],
            "lat": raw_place['coordinates']['lat']
        },
    )

    if created:
        print(f"✅ Место создано: {place.title}")
    else:
        print(f"🔁 Место уже существует: {place.title}")

    for img_url in raw_place['imgs']:
        response = requests.get(img_url)
        response.raise_for_status()
        content = ContentFile(response.content)
        img_name = get_filename_from_url(img_url)
        image_object = Image.objects.create(place=place)
        image_object.image.save(name=img_name, content=content, save=True)
        print(f" Загружено изображение: {img_name}")


def load_places_from_folder(folder):
    place_paths = [
        os.path.join(folder, filename) for filename in os.listdir(folder)
        if filename.endswith(".json")
    ]

    for path in place_paths:
        with open(Path(path), 'r', encoding='utf-8') as raw_file:
            raw_place = json.load(raw_file)
        load_place_from_data(raw_place)


def load_place_from_url(url):
    print(f" Загрузка: {url}")
    response = requests.get(url)
    response.raise_for_status()
    raw_place = response.json()
    load_place_from_data(raw_place)


class Command(BaseCommand):
    help = 'Загружает места из JSON-файлов (папка или URL)'

    def add_arguments(self, parser):
        parser.add_argument('-j', '--places_dir', help='Путь к папке с JSON-файлами')
        parser.add_argument('-u', '--place_url', help='URL JSON-файла для загрузки')

    def handle(self, *args, **options):
        places_dir = options.get('places_dir')
        place_url = options.get('place_url')

        if place_url:
            load_place_from_url(place_url)
        elif place_url:
            load_places_from_folder(places_dir)
        else:
            self.stderr.write(self.style.ERROR(
                'Укажи либо --places_dir, либо --place_url для загрузки.'))
