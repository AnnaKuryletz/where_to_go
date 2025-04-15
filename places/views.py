from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from places.models import Place


def index(request):
    features = []
    for place in Place.objects.all():
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [place.lng, place.lat]},
                "properties": {
                    "title": place.title,
                    "placeId": place.id,
                    "detailsUrl": reverse("place_json", args=[place.id]),
                },
            }
        )

    context = {"geo_json": {"type": "FeatureCollection", "features": features}}

    return render(request, "start_page.html", context)


def place_detail_json(request, place_id):
    place = get_object_or_404(Place, pk=place_id)

    place_json = {
        "title": place.title,
        "imgs": [image.image.url for image in place.images.all()],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {"lng": place.lng, "lat": place.lat},
    }

    return JsonResponse(
        place_json, json_dumps_params={"ensure_ascii": False, "indent": 2}
    )
