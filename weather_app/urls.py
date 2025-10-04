from django.urls import path

from . import views
from . import views_static_debug

urlpatterns = [
    path("", views.index, name="index"),
    path("static-debug/", views_static_debug.static_debug, name="static_debug"),
]
