import os
from django.conf import settings
from django.http import HttpResponse

def static_debug(request):
    static_root = os.path.join(settings.BASE_DIR, 'weather_app', 'static', 'weather_app')
    files = os.listdir(static_root)
    return HttpResponse('<br>'.join(files))
