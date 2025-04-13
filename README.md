# 🌍 Where to Go — Интерактивная карта интересных мест Москвы

Проект помогает отображать интересные места Москвы на карте. Контент можно удобно заполнять через админку, включая изображения и описание мест.

![image](https://github.com/user-attachments/assets/fe299dca-3e88-486d-8fb8-978d94eac827)


## 🚀 Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/your-username/where-to-go.git
cd where-to-go
```
### 2. Установи зависимости
Создай и активируй виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
```
Установи зависимости:

```bash
pip install -r requirements.txt
```
### 3. Создай файл `.env`
```dotenv
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=db.sqlite3
```
### 4. Примени миграции и запусти сервер
```bash
python manage.py migrate
python manage.py runserver
```
## ⚙️ Стек технологий
`Python 3.11+`

`Django 5.2`

`SQLite (по умолчанию) или PostgreSQL`

`Django Admin`

`django-tinymce — WYSIWYG`-редактор в админке

`django-admin-sortable2` — сортировка изображений

`environs` — управление переменными окружения
