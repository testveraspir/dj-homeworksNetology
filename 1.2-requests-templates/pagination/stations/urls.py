from django.urls import path

from .views import index, bus_stations_view

urlpatterns = [
    path('', index, name='index'),
    path('bus_stations/', bus_stations_view, name='bus_stations'),
]
