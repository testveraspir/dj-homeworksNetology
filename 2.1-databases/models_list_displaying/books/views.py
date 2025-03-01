from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    book_objects = Book.objects.all()
    context = {'books': book_objects}
    return render(request, template, context)


def books_by_pub_date_view(request, pub_date):
    template = 'books/books_by_pub_date.html'
    book_objects = Book.objects.filter(pub_date=pub_date)

    previous_book = Book.objects.filter(pub_date__lt=pub_date)
    previous_book = previous_book.order_by('-pub_date').first()
    previous_date = previous_book.pub_date if previous_book else None

    next_book = Book.objects.filter(pub_date__gt=pub_date)
    next_book = next_book.order_by('pub_date').first()
    next_date = next_book.pub_date if next_book else None

    context = {
        'books': book_objects,
        'previous_date': previous_date,
        'next_date': next_date,
    }
    return render(request, template, context)
