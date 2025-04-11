from django.http import HttpResponse
from django.template import loader
from places.models import Place

def index(request):
    template = loader.get_template('start_page.html')

    features = []
    for place in Place.objects.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.lng, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.placeId,
                "detailsUrl": place.detailsUrl
            }
        })

    context = {
        "geo_json": {
            "type": "FeatureCollection",
            "features": features
        }
    }

    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
