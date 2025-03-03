from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def get_sort_param(sort_param):
    if sort_param == 'name':
        return 'name'
    elif sort_param == 'min_price':
        return 'price'
    elif sort_param == 'max_price':
        return '-price'
    else:
        raise ValueError(f'Некорректный параметр сортировки: {sort_param}')


def show_catalog(request):
    try:
        template = 'catalog.html'
        phone_objects = Phone.objects.all()
        sort = request.GET.get('sort', 'name')
        sort_name = get_sort_param(sort)
        phone_objects = phone_objects.order_by(sort_name)
        context = {'phones': phone_objects}
        return render(request, template, context)
    except ValueError as e:
        print(f'Ошибка: {e}')
        return HttpResponse(e)
    except Exception as ex:
        print(f'Ошибка: {ex}')
        return HttpResponse("Ошибка при сортировке!")


def show_product(request, slug):
    template = 'product.html'
    try:
        phone = Phone.objects.get(slug=slug)
        context = {'phone': phone}
        return render(request, template, context)
    except ObjectDoesNotExist:
        return HttpResponse("Телефон не найден!")
