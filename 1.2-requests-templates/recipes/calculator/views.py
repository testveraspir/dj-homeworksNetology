from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'salad': {
        'помидор, шт': 1,
        'огурец, шт': 1,
        'редиска, шт': 2,
        'соус, ложка': 1,
        'хлеб, ломтик': 1,
    },
    'miso': {
        'мисо-паста, ложка': 0.5,
        'водросли-вакаме, ч.л.': 0.25,
        'вода, л.': 0.4,
        'соевый-соус, ч.л.': 1,
        'тофу, г.': 50,
    },
}


def get_recipe_with_servings(dish, servings):
    for ingredient, count in dish.items():
        dish[ingredient] = count * servings
    return dish


def hello_view(request):
    context = {
        'dishes': list(DATA)
    }
    return render(request, 'calculator/hello.html', context)


def recipe_view(request, name):
    servings = int(request.GET.get('servings', 1))
    if DATA.get(name) is None:
        return HttpResponse(f'Блюда {name} на сервере нет.<br><a href="/">Вернуться на главную</a>')
    data = get_recipe_with_servings(DATA.get(name), servings)
    context = {
        'recipe': data
        }
    return render(request, 'calculator/index.html', context)


def recipe_count_view(request, name, servings):
    data = get_recipe_with_servings(DATA[name], servings)

    context = {
        'recipe': data,
    }
    return render(request, 'calculator/index.html', context)
