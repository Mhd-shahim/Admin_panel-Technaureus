from django.urls import path
from . views import ListAllAuthor,ListAllBook

urlpatterns=[
    path('authors', ListAllAuthor.as_view() ),
    path('books', ListAllBook.as_view()),
]
