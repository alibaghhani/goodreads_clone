from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from .pagination import CustomPagination
from books.models import Book, Genre, Rate
from books.serializers import BookSerializer, GenreSerializer, RateSerializer


class BooksViewSet(ModelViewSet):
    '''
    This view produces a series of endpoints for us by default
    '''
    queryset = Book.objects.all()
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''
        This method helps us to implement sort and search

        '''
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

    def create(self, request, *args, **kwargs):
        '''
        This method creates a new book
        '''

        serializer = BookSerializer(data=request.data)
        rate_serializer = RateSerializer(data=request.data, context={'request': request})
        if request.user.is_superuser:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            if rate_serializer.is_valid():
                book = rate_serializer.validated_data.get('book')
                if Rate.objects.filter(user=request.user, book=book).exists():
                    return Response({'message': 'you ave already rated this book'})
                else:
                    rate_serializer.save()
                    return Response(rate_serializer.data, status=201)
            else:
                return Response(rate_serializer.errors, status=400)


class GenreViewSet(BooksViewSet):
    '''
    This class does the same think as the Book viewset
    '''

    def get_permissions(self):
        '''
        This method hellp us to manage users
        in this method we determined that
        admins can add genre but regular users don't
        '''
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        '''
        This method returns a list of all books
        '''
        queryset = Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        '''
        This method creates a new genre
        '''
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
