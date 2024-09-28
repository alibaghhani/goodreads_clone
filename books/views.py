

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from books.models import Book
from books.serializers import BookSerializer


class BooksViewSet(ViewSet):
    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
