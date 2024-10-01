from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book, Genre, Rate
from authentication.models import User
from .serializers import BookSerializer


class BookTests(APITestCase):
    """
    This class is for test the endpoints

    how to run: python manage.py test
    """

    def setUp(self):
        """
        This method creates the basic needs to running tests

        self.client = Extends Django's existing Client class .
        about client class: https://docs.djangoproject.com/en/5.1/topics/testing/tools/#the-test-client

        self.admin = creates superuser for objects that superuser should create itself
        self.user = creates normal user for objects that normal user should create itself
        self.genre = creates genre (It will be needed later to make a book object)
        self.book_data = creates data for creating a book object
        self.book = creates book object


        self.base_url = It refers to the book's endpoints
        self.genre_base_url = It refers to the genre's endpoints

        """
        # -----------users & admin------------#
        self.client = APIClient()
        self.admin = User.objects.create_superuser(username='test admin', password='test password',
                                                   email='test@gmail.com')
        self.user = User.objects.create(username='test user', password='test password')
        self.client.force_authenticate(user=self.user)
        # -------------------------------------#

        # ------books & genres-------#
        self.genre = Genre.objects.create(name='test genre')
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'description': 'Test Description',
            'genre': 1
        }

        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            description='Test Description',
            genre=self.genre
        )
        # ----------------------------#

        # ---------url--------------#
        self.base_url = reverse('books-list')
        self.genre_base_url = reverse('genres-list')
        # ----------------------------#

    def test_list_books(self):
        """
        This method tests list of books
        """
        response = self.client.get(self.base_url)
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_create_book_as_admin(self):
        """
        This method tests creating a book as admin so it should returns 201 status code
        """
        self.client.force_authenticate(self.admin)
        self.client.force_login(self.admin)
        response = self.client.post(self.base_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_as_regular_user(self):
        """
        This method tests creating a book as a regular user so it should returns 400 status code

        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.base_url, self.book_data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rate_to_book(self):
        """
        This method tests rate to a book as a regular user so it should returns 201 status code and saves rate to the database

        """
        self.client.force_authenticate(self.user)
        self.client.force_login(self.user)
        response = self.client.post(f'{self.base_url}', {'book': 1, 'rate': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
        self.assertEqual(Rate.objects.filter(book=self.book, user=self.user).first().rate, 5)

    def test_create_genre_as_admin(self):
        """
        This method tests creating a genre as admin so it should returns 201 status code

        """
        self.client.force_authenticate(self.admin)
        self.client.force_login(self.admin)
        response = self.client.post(self.genre_base_url, {'name': 'math'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_genre_as_user(self):
        """
        This method tests creating a genre as a regular user so it should returns 400 status code

        """
        self.client.force_authenticate(self.user)
        response = self.client.post(self.genre_base_url, {'name': 'english'}, format='json')
        self.assertNotEqual(response.data, status.HTTP_201_CREATED)
