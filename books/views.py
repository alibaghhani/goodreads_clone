from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book, Genre
from books.serializers import BookSerializer, GenreSerializer


class BooksViewSet(ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action == 'list':
            return [IsAuthenticated()]
        return super().get_permissions()

    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GenreViewSet(ViewSet):
    permission_classes = [AllowAny]

    def list(self):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)
