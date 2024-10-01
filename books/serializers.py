from django.http import HttpRequest
from rest_framework.serializers import ModelSerializer
from books.models import Book, Genre, Rate


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description','genre')


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = ('book', 'rate')

    def create(self, validated_data):
        request:HttpRequest = self.context.get('request')
        user = request.user
        rate = validated_data.get('rate')
        rate, created = Rate.objects.get_or_create(book=validated_data['book'], user=user, rate=rate)
        return rate
