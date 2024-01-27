from django.db import models

# Create your models here.
class Author(models.Model):
    authorname = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.authorname
