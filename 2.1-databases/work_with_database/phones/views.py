from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    phone_objects = Phone.objects.all()
    sort = request.GET.get('sort', 'name')
    if sort == 'name':
        phone_objects = phone_objects.order_by("name")
    elif sort == 'min_price':
        phone_objects = phone_objects.order_by("price")
    elif sort == 'max_price':
        phone_objects = phone_objects.order_by("-price")
    else:
        return HttpResponse("Ошибка при сортировке!")
    context = {'phones': phone_objects}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    try:
        phone = Phone.objects.get(slug=slug)
        context = {'phone': phone}
        return render(request, template, context)
    except ObjectDoesNotExist:
        return HttpResponse("Телефон не найден!")
