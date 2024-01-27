from django.db import models
from authors.models import Author
# Create your models here.

class Book(models.Model):
    book_id = models.CharField(max_length=10,)
    book_name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    

    def __str__(self):
        return self.book_name