from django.shortcuts import render,redirect, get_object_or_404
from .models import Book
from authors.models import Author
from django.contrib import messages
from django import forms
import random
import string

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def books(request):
    if 'username' in request.session:
        all_books, all_authors = Book.objects.all(), Author.objects.all()
        total_books, total_authors = len(all_books), len(all_authors)
        queryset = request.POST.get('search', '')

        if queryset:
            book_list = Book.objects.filter(book_name__icontains=queryset)
        else:
            book_list = Book.objects.all()

        paginator = Paginator(book_list, 5) 
        page = request.GET.get('page')

        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

    
        context = {'books': books,
                'total_authors': total_authors,
                'total_books': total_books
                }
        return render(request, 'books.html', context)
    else:
        return redirect('Login')


def generate_random_book_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=8))

def addBook(request):
    if request.method == 'POST':
        author_name = request.POST.get('authorname')
        book_name = request.POST.get('bookname')
        
        try:
            author = Author.objects.get(authorname=author_name)
        except Author.DoesNotExist:
            messages.info(request, "Author doesn't exist")
            return redirect('Books')

        if author and book_name:
            if Book.objects.filter(book_name=book_name).exists():
                messages.info(request, "A book with the same name already exists.")
                return redirect('Books')
            else:
                book_id = generate_random_book_id()
                new_book = Book.objects.create(book_name=book_name, book_id=book_id, author=author)
                print("Object created:", new_book)
                return redirect('Books')
        else:
            messages.info(request, "*All fields are required")
            return redirect('Books')
        
def editBook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        author_name = request.POST.get('authorname')
        book_name = request.POST.get('bookname')
       
        if author_name and book_name:
            if Book.objects.filter(book_name=book_name).exists():
                messages.info(request, "A book with the same name already exists.")
                return redirect('Books')
            else:
                if Author.objects.filter(authorname=author_name).exists():
                    book.author.authorname = author_name
                    book.book_name = book_name
                    book.save()
                else:
                    messages.info(request, "No such author exists")
                    return redirect('Books')
            return redirect('Books')
    else:
        return render(request, 'Books.html', {'book': book})  
    
class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['status']


def updateStatus(request, book_id):
    book_instance = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        form = BookModelForm(request.POST, instance=book_instance)
        if form.is_valid():
            book_instance.status = form.cleaned_data['status']
            book_instance.save() 
            return redirect('Books')  
    else:
        form = BookModelForm(instance=book_instance)
        return render(request, 'book.html')









    