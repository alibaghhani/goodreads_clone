from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .pagination import CustomPagination
from books.models import Book, Genre
from books.serializers import BookSerializer, GenreSerializer


class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    serializer_class = BookSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        kw = self.request.query_params.get('kw')
        if kw:
            queryset = queryset.filter(Q(title__contains=kw) | Q(description__contains=kw))
        order = self.request.query_params.get('order')
        if order is not None:
            fields = ['id', '-id', 'title', 'author']
            if order in fields:
                queryset = queryset.order_by(order)
            else:
                raise ValidationError({'errror': f'order field must be in {fields}'})
        return queryset


class GenreViewSet(BooksViewSet):

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
