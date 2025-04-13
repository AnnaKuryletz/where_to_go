from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase


class ImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Image
    readonly_fields = ["preview"]
    fields = ["image", "preview", "position"]
    extra = 0

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.image.url)
        return "Нет изображения"
    
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["title"]
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["display_image_info"]
    ordering = ["position"]

    @admin.display(description='IMAGE')
    def display_image_info(self, obj):
        return f"{obj.position} {obj.place}"
