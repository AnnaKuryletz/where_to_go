from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
 
from where_to_go import views
 
 
urlpatterns = [
    path('', views.index),
    path('places/<int:place_id>', views.place_detail_json, name="place_json"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)