from django.db import models
from core.models import TimeStampMixin


# Create your models here.
class Book(TimeStampMixin):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
