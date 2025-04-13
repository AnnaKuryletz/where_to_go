from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField(blank=True, verbose_name="Краткое описание")
    description_long = HTMLField(verbose_name="Подробное описание")
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")
    placeId = models.CharField("placeId", null=True, blank=True, max_length=200)
    detailsUrl = models.CharField(
        "detailsUrl",
        null=True,
        blank=True,
        max_length=200,
        default="/static/places/details-placeholder.json",
    )

    def __str__(self):
        return self.title


class Image(models.Model):
    position = models.SmallIntegerField(
        default=0, verbose_name="Позиция", db_index=True
    )
    image = models.ImageField(verbose_name="Картинка")
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name="images", verbose_name="Место"
    )

    def __str__(self):
        return f"Картинка для {self.place}"

    class Meta:
        ordering = ["position"]
