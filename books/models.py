from django.db import models
from core.models import TimeStampMixin


# Create your models here.
class Book(TimeStampMixin):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class Genre(TimeStampMixin):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

