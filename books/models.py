from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from authentication.models import User
from core.models import TimeStampMixin


# Create your models here.
class Book(TimeStampMixin):
    '''
    This is The Book model
    for creating objects in database

    ----fields----
    title = models.CharField(max_length=100) ----> book title --> type: character(string)
    author = models.CharField(max_length=100) ----> author name --> type: character(string)
    description = models.TextField() ----> book's description --> type: character(string) without character limit
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='books') ---> sql foreinkey
    --------------
    '''
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class Genre(TimeStampMixin):
    '''
       This model is
       for creating genre objects in database

       ----fields----
       name = models.CharField(max_length=100) ----> book title --> type: character(string)
       --------------
       '''
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Rate(TimeStampMixin):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    rate = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])


