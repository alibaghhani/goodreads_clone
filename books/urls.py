from django.urls import path
from .views import BooksViewSet, GenreViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'books',
    BooksViewSet,
    basename='books'
)

router.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)


urlpatterns = [

]
urlpatterns += router.urls