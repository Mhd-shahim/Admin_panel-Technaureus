from django.urls import path
from authors import views

urlpatterns = [
   path('',views.authors, name='Authors'),
   path('add-author', views.addAuthor, name='add_author'),
   path('edit-author/<int:author_id>/', views.editAuthor, name='edit_author'),
   path('detailed-author/<int:author_id>', views.singleAuthor, name='detailed_author'),
   path('edit-detailed-author/<int:book_id>', views.editBook, name='edit_detailed_author'),
   path('status-author/<int:author_id>', views.updateStatus, name='status_update'),
   path('status-book-single-author/<int:book_id>', views.updateStatusBook, name='status_update_book_single_author')
]


