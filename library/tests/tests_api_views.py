import json

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from library.models import Genre, Author, Book, Library, Comment

client = APIClient()


class TestBooksAPIViews(APITestCase):
    '''
    Тестирует работу представлений книг
    '''
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create(
            username='user1',
            password='pass1'
        )
        self.user_1_token = Token.objects.create(user=self.user_1)
        user_2 = get_user_model().objects.create(
            username='user2',
            password='pass2'
        )
        self.user_2_token = Token.objects.create(user=user_2)
        library = Library.objects.create(
            title='Библиотека',
            address='Дом и улица',
            working_hours='09:12-23:14'
        )
        genre = Genre.objects.create(
            title='Жанр'
        )
        author = Author.objects.create(
            full_name='Автор',
            birthday=1495
        )
        self.book = Book.default_manager.create(
            owner=self.user_1,
            title='Книга',
            year=1510,
            library=library,
            author=author,
            genre=genre
        )

    def test_get_books_list(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = client.get('/api/v1/books/')
        data = [{
            "title": "Книга",
            "owner": 1,
            "year": 1510,
            "genre": 1,
            "author": 1
        }]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_create_book(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "title": "Книга 2",
            "year": 2003,
            "genre": 1,
            "author": 1
        }
        created_data = {
            "owner": 1,
            "title": "Книга 2",
            "year": 2003,
            "genre": 1,
            "author": 1
        }
        response = client.post('/api/v1/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), created_data)

    def test_get_book(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "title": "Книга",
            "owner": 1,
            "year": 1510,
            "genre": 1,
            "author": 1
        }
        response = client.get('/api/v1/books/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_put_update_book(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "title": "Измененная книга",
            "owner": 1,
            "year": 2003,
            "genre": 1,
            "author": 1
        }
        response = client.put('/api/v1/books/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)
        response = client.put('/api/v1/books/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_update_book(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "title": "Измененная книга 2"
        }
        full_data = {
            "title": "Измененная книга 2",
            "owner": 1,
            "year": 1510,
            "genre": 1,
            "author": 1
        }
        response = client.patch('/api/v1/books/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), full_data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)
        response = client.put('/api/v1/books/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)
        response = client.delete('/api/v1/books/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = client.delete('/api/v1/books/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestGenresAPIViews(APITestCase):
    '''
    Тестирует работу представлений жанров
    '''
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create(
            username='user1',
            password='pass1'
        )
        self.user_1_token = Token.objects.create(user=self.user_1)
        genre = Genre.objects.create(
            title='Жанр'
        )

    def test_genres_list(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = client.get('/api/v1/genres/')
        data = [{
            "id": 1,
            "title": "Жанр",
        }]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_get_genre(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "id": 1,
            "title": "Жанр",
        }
        response = client.get('/api/v1/genres/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)


class TestAuthorsAPIViews(APITestCase):
    '''
    Тестирует работу представлений авторов
    '''
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create(
            username='user1',
            password='pass1'
        )
        self.user_1_token = Token.objects.create(user=self.user_1)
        author = Author.objects.create(
            full_name='Автор',
            birthday=1495
        )

    def test_authors_list(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = client.get('/api/v1/authors/')
        data = [{
            "id": 1,
            "full_name": "Автор",
            "birthday": 1495
        }]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)


class TestCommentsAPIViews(APITestCase):
    '''
    Тестирует работу представлений комментариев
    '''
    def setUp(self) -> None:
        self.user_1 = get_user_model().objects.create(
            username='user1',
            password='pass1'
        )
        self.user_1_token = Token.objects.create(user=self.user_1)
        user_2 = get_user_model().objects.create(
            username='user2',
            password='pass2'
        )
        self.user_2_token = Token.objects.create(user=user_2)
        library = Library.objects.create(
            title='Библиотека',
            address='Дом и улица',
            working_hours='09:12-23:14'
        )
        genre = Genre.objects.create(
            title='Жанр'
        )
        author = Author.objects.create(
            full_name='Автор',
            birthday=1495
        )
        self.book = Book.default_manager.create(
            owner=self.user_1,
            title='Книга',
            year=1510,
            library=library,
            author=author,
            genre=genre
        )
        self.comment_1 = Comment.active.create(
            owner=self.user_1,
            book=self.book,
            text="Тест",
        )

    def test_get_comments_list(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = client.get('/api/v1/books/1/comments/')
        data = [{
            "id": 1,
            "owner": 1,
            "book": 1,
            "text": "Тест",
            "created_at": self.comment_1.created_at.strftime(format='%Y-%m-%dT%H:%M:%S.%fZ')
        }]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_create_comment(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "book": 1,
            "text": "Новый текст"
        }

        response = client.post('/api/v1/books/1/comments/', data, format='json')
        comment_2 = Comment.active.get(text="Новый текст")
        created_data = {
            "id": 2,
            "owner": 1,
            "book": 1,
            "text": "Новый текст",
            "created_at": comment_2.created_at.strftime(format='%Y-%m-%dT%H:%M:%S.%fZ')
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), created_data)

    def test_get_comment(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "id": 1,
            "owner": 1,
            "book": 1,
            "text": "Тест",
            "created_at": self.comment_1.created_at.strftime(format='%Y-%m-%dT%H:%M:%S.%fZ')
        }
        response = client.get('/api/v1/books/1/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_put_update_comment(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "id": 1,
            "owner": 1,
            "book": 1,
            "text": "Измененный текст",
            "created_at": self.comment_1.created_at.strftime(format='%Y-%m-%dT%H:%M:%S.%fZ')
        }
        response = client.put('/api/v1/books/1/comments/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)
        response = client.put('/api/v1/books/1/comments/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_update_comments(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        data = {
            "text": "Измененный текст"
        }
        full_data = {
            "id": 1,
            "owner": 1,
            "book": 1,
            "text": "Измененный текст",
            "created_at": self.comment_1.created_at.strftime(format='%Y-%m-%dT%H:%M:%S.%fZ')
        }
        response = client.patch('/api/v1/books/1/comments/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), full_data)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)
        response = client.put('/api/v1/books/1/comments/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_2_token.key)
        response = client.delete('/api/v1/books/1/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = client.delete('/api/v1/books/1/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
