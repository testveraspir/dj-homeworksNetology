from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    book_objects = Book.objects.all()
    context = {'books': book_objects}
    return render(request, template, context)
