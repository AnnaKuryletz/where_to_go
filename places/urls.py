# places/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("tinymce/", include("tinymce.urls")),
    path("places/<str:place_id>/", views.place_detail_json, name="place_json"),
]
