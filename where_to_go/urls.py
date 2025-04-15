from django.contrib import admin
from django.urls import path

from places import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("places/<str:place_id>/", views.place_detail_json, name="place_json"),  
] 
