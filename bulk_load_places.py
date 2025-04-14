import os
import subprocess
from urllib.parse import quote

BASE_URL = "https://annakurilec.pythonanywhere.com"
LOCAL_DIR = "/home/AnnaKurilec/annakurilec.pythonanywhere.com/static/places"

def get_json_files(directory):
    return [
        f for f in os.listdir(directory)
        if f.endswith(".json")
    ]

def main():
    json_files = get_json_files(LOCAL_DIR)

    for json_file in json_files:
        encoded_name = quote(json_file)
        full_url = f"{BASE_URL}/{encoded_name}"
        print(f"\n📦 Загрузка: {json_file}")
        subprocess.run(["python", "manage.py", "load_place", full_url])

if __name__ == "__main__":
    main()
