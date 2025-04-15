from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from places import views


urlpatterns = (
    [
        path("", views.index),
        path("tinymce/", include("tinymce.urls")),
        path("places/<str:place_id>/", views.place_detail_json, name="place_json"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
