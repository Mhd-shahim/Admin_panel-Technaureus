from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author
from books.models import Book
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
import string,random
# Create your views here.


def authors(request):
    if 'username' in request.session:
        queryset = Author.objects.all()
        all_books = Book.objects.all()
        total_books,total_authors = len(all_books),len(queryset)

        if request.method == 'POST':
            search_query = request.POST.get('search')
            if search_query:
                queryset = queryset.filter(authorname__icontains=search_query)

        paginator = Paginator(queryset, 5)  

        page_number = request.GET.get('page')
        try:
            authors = paginator.page(page_number)
        except PageNotAnInteger:
            authors = paginator.page(1)
        except EmptyPage:
            authors = paginator.page(paginator.num_pages)

        context = {
            'authors': authors,
            'total_books': total_books,
            'total_authors': total_authors 
        }
        return render(request, 'authors.html', context)
    else:
        return redirect('Login')
    

def addAuthor(request):
    if request.method == 'POST':
        Author_name = request.POST.get('authorname')
        Username = request.POST.get('username')
        email = request.POST.get('email')
   
        if Author_name and Username and email: 
            if Author.objects.filter(authorname=Author_name).exists():
                messages.info(request, "An author with the same name already exists.")

            elif Author.objects.filter(username=Username).exists():
                messages.info(request, "An author with the same User name already exists.")

            elif Author.objects.filter(email=email).exists():
                messages.info(request, "An author with the same email already exists.")    
            else:
                new_author = Author.objects.create(authorname=Author_name, username=Username, email=email)
                print("Object created:", new_author)
        else:
           messages.info(request, "*All fields are required")
    return redirect('Authors')
    
    
def editAuthor(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    
    if request.method == 'POST':
        authorname = request.POST.get('authorname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        if authorname and username and email:
            if Author.objects.filter(authorname=authorname).exists():
                messages.info(request, "An author with the same name already exists.")
                return redirect('Authors')
            elif Author.objects.filter(username=username).exists():
                messages.info(request, "An author with the same User name already exists.")
                return redirect('Authors')
            elif Author.objects.filter(email=email).exists():
                messages.info(request, "An author with the same email already exists.") 
                return redirect('Authors')
            else:
                author.authorname = authorname
                author.username = username
                author.email = email
                author.save()
                return redirect('Authors')
    else:
        return render(request, 'author.html', {'author': author})  



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def singleAuthor(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    queryset = request.POST.get('search', '')

    if queryset:
        book_list = Book.objects.filter(author=author, book_name__icontains=queryset)
    else:
        book_list = Book.objects.filter(author=author)
    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage: 
        books = paginator.page(paginator.num_pages)
    context = {'author': author, 'books': books}
    return render(request, 'single_author.html', context)



class AuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['status']


def updateStatus(request, author_id):
    author_instance = get_object_or_404(Author, pk=author_id)
    
    if request.method == 'POST':
        form = AuthorModelForm(request.POST, instance=author_instance)
        if form.is_valid():
            author_instance.status = form.cleaned_data['status']
            author_instance.save() 
            return redirect('Authors')
    else:
        form = AuthorModelForm(instance=author_instance)
        return render(request, 'author.html', {'form': form, 'author_id': author_id})

def generate_random_book_id():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=8))

def addBook_Author(request):
    if request.method == 'POST':
        author_name = request.POST.get('authorname')
        book_name = request.POST.get('bookname')
        
        try:
            author = Author.objects.get(authorname=author_name)
        except Author.DoesNotExist:
            messages.info(request, "Author doesn't exist")
            return redirect(f'/authors/detailed-author/{author.id}')

        if author and book_name:
            if Book.objects.filter(book_name=book_name).exists():
                messages.info(request, "A book with the same name already exists.")
                return redirect(f'/authors/detailed-author/{author.id}')
            else:
                book_id = generate_random_book_id()
                new_book = Book.objects.create(book_name=book_name, book_id=book_id, author=author)
                print("Object created:", new_book)
                return redirect(f'/authors/detailed-author/{author.id}')
        else:
            messages.info(request, "*All fields are required")
            return redirect(f'/authors/detailed-author/{author.id}')


def editBook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        author_name = request.POST.get('authorname')
        book_name = request.POST.get('bookname')
       
        if author_name and book_name:
            if Book.objects.filter(book_name=book_name).exists():
                messages.info(request, "A book with the same name already exists.")
                return redirect(f'/authors/detailed-author/{book.author.id}')
            else:
                book.author.authorname = author_name
                book.book_name = book_name
                book.save()
                return redirect(f'/authors/detailed-author/{book.author.id}')
    else:
        return render(request, 'single_author.html', {'book': book})
    
class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['status']


def updateStatusBook(request, book_id):
    book_instance = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        form = BookModelForm(request.POST, instance=book_instance)
        if form.is_valid():
            book_instance.status = form.cleaned_data['status']
            book_instance.save() 
            return redirect(f'/authors/detailed-author/{book_instance.author.id}') 
    else:
        form = BookModelForm(instance=book_instance)
        return render(request, 'single_author.html',)



