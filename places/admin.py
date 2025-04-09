from django.contrib import admin
from .models import Place, Image


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["display_image_info"]
    ordering = ["position"]

    @admin.display(description='IMAGE')
    def display_image_info(self, obj):
        return f"{obj.position} {obj.place}"
