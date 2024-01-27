from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics,filters
from authors.models import Author
from books.models import Book
from .seriralizers import AuthorSerializer,BookSerializer


class ListAllAuthor(generics.ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['authorname', 'username', 'email']  
    queryset = Author.objects.filter(status=True)

class ListAllBook(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.filter(status=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['book_name']



