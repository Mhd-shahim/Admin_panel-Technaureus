from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='Books'),
    path('add-book', views.addBook, name='add_book'),
    path('edit-book/<int:book_id>/', views.editBook, name='edit_book'),
    path('status-book/<int:book_id>', views.updateStatus, name='status_update_book'),
    
]