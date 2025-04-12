from django.http import HttpResponse
from django.template import loader
from places.models import Place
from django.shortcuts import get_object_or_404


def index(request):
    template = loader.get_template("start_page.html")

    features = []
    for place in Place.objects.all():
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [place.lng, place.lat]},
                "properties": {
                    "title": place.title,
                    "placeId": place.placeId,
                    "detailsUrl": place.detailsUrl,
                },
            }
        )

    context = {"geo_json": {"type": "FeatureCollection", "features": features}}

    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    return HttpResponse(place.title)
