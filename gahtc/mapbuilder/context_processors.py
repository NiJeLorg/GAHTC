from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_API_KEY': settings.GOOGLE_MAPS_API,
        'MAPBOX_ACCESS_TOKEN': settings.MAPBOX_ACCESS_TOKEN
    }