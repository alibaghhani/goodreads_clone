from rest_framework.serializers import ModelSerializer
from books.models import Book, Genre


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description')


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')
