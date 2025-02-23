import csv

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination import settings


def index(request):
    return redirect(reverse('bus_stations'))


def get_bus_stations_from_csv(name_file):
    try:
        with open(name_file, newline='', encoding='utf-8') as csvfile:
            list_bus_stations = []
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = {'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
                list_bus_stations.append(data)
    except Exception as e:
        print(f"Ошибка при обработке файла csv {e}")
        return -1
    return list_bus_stations


def bus_stations_view(request):
    bus_stations = get_bus_stations_from_csv(settings.BUS_STATION_CSV)
    if bus_stations == -1:
        return HttpResponse("Ошибка при обработке файла csv!")
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(bus_stations, 10)
    page = paginator.get_page(page_number)
    bus_stations_10 = page.object_list
    context = {
         'bus_stations': bus_stations_10,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
