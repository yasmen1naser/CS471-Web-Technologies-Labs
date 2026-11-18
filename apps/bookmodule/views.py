from .models import Book
from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Max, Min
from .models import Student, Address
from django.db.models import (
    F,Value, FloatField, ExpressionWrapper,
    OuterRef, Subquery)
from .models import Book, Publisher

def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        book_count=Count(
            'books',
            filter=Q(
                books__price__gt=50,
                books__quantity__lt=5,
                books__quantity__gte=1
            )
        )
    )

    return render(request, 'bookmodule/lab9_task6.html', {
        'publishers': publishers
    })
def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        highly_rated_count=Count(
            'books',
            filter=Q(books__rating__gte=4)
        ),
        highly_rated_quantity=Sum(
            'books__quantity',
            filter=Q(books__rating__gte=4)
        )
    )

    return render(request, 'bookmodule/lab9_task5.html', {
        'publishers': publishers
    })
def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        average_price=Avg('books__price'),
        minimum_price=Min('books__price'),
        maximum_price=Max('books__price')
    )

    return render(request, 'bookmodule/lab9_task4.html', {
        'publishers': publishers
    })
def lab9_task3(request):
    oldest_books = Book.objects.filter(
        publisher=OuterRef('pk'),
        pubdate__isnull=False
    ).order_by('pubdate')

    publishers = Publisher.objects.annotate(
        oldest_book_title=Subquery(
            oldest_books.values('title')[:1]
        ),
        oldest_book_date=Subquery(
            oldest_books.values('pubdate')[:1]
        )
    )

    return render(request, 'bookmodule/lab9_task3.html', {
        'publishers': publishers
    })
def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_stock=Sum('books__quantity')
    )

    return render(request, 'bookmodule/lab9_task2.html', {
        'publishers': publishers
    })
def lab9_task1(request):
    total = Book.objects.aggregate(total=Sum('quantity'))['total'] or 0

    if total > 0:
        books = Book.objects.annotate(
            availability=ExpressionWrapper(
                F('quantity') * 100.0 / Value(total),
                output_field=FloatField()
            )
        )
    else:
        books = Book.objects.annotate(
            availability=Value(0.0, output_field=FloatField())
        )

    return render(request, 'bookmodule/lab9_task1.html', {
        'books': books
    })
def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8_book_list.html', {
        'books': books,
        'heading': 'Books with Price Less Than or Equal to 80'
    })
def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) &
        (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_book_list.html', {
        'books': books,
        'heading': "Books with Edition Higher Than 3 and Title or Author Contains 'qu'"
    })
def lab8_task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) &
        ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_book_list.html', {
        'books': books,
        'heading': "Books with Edition Not Higher Than 3 and Title or Author Does Not Contain 'qu'"
    })
def lab8_task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/lab8_book_list.html', {
        'books': books,
        'heading': 'Books Ordered by Title'
    })
def lab8_task5(request):
    result = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        maximum_price=Max('price'),
        minimum_price=Min('price')
    )

    return render(request, 'bookmodule/lab8_task5.html', result)
def lab8_task7(request):
    cities = Address.objects.annotate(
        student_count=Count('students')
    )

    return render(request, 'bookmodule/lab8_task7.html', {'cities': cities})
def index(request):
    return render(request, "bookmodule/index.html")
def list_books(request):
    return render(request, "bookmodule/list_books.html")
def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")
def aboutus(request):
    return render(request, "bookmodule/aboutus.html")
def index2(request, val1):
    return render(request, "bookmodule/index.html")
def html5_links(request):
    return render(request, 'books/html5/links.html')
def html5_formatting(request):
    return render(request, 'books/html5/formatting.html')
def html5_listing(request):
    return render(request, 'books/html5/listing.html')
def html5_tables(request):
    return render(request, 'books/html5/tables.html')

def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword', '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='delivery')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(
        author__isnull=False
    ).filter(
        title__icontains='and'
    ).filter(
        edition__gte=2
    ).exclude(
        price__lte=100
    )[:10]

    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')