import json
import uuid
import random
from pathlib import Path

from django.contrib.auth import get_user_model

from library.models import Library, Genre, Author, Book, Comment


class DatabaseStuffer():
    def fill(self):
        '''
        Заполняет базу данных тестовыми данными
        '''
        try:
            self._fill_users()
            self._fill_library()
            self._fill_genres()
            self._fill_authors_and_books()
            self._fill_comments()
            print('Все данные успешно загружены!')
        except Exception as e:
            print(f'Что-то пошло нет так\nСообщение об ошибке: {e}')

    def _fill_users(self) -> None:
        '''
        Создаёт 100 случайно сгенерированных пользователей
        '''
        for i in range(100):
            get_user_model().objects.create(
                username=f'user_{i}',
                password=uuid.uuid4(),
            )

    def _fill_library(self):
        for i in range(5):
            Library.objects.create(
                title=f'Районная библиотека №{i+1}',
                address=f'г. Рыбинск, улица {uuid.uuid4()}, дом {i}',
                working_hours='09:00 - 17:00'
            )

    def _fill_genres(self):
        genres = ['Детектив', 'Приключение', 'Роман', 'Фентези', 'Научная фантастика', 'Справочник']
        for genre in genres:
            Genre.objects.create(
                title=genre
            )

    def _fill_authors_and_books(self):
        file_path = f'{Path(__file__).resolve().parent.parent}/data/authors_books.json'
        library = Library.objects.first()
        users = get_user_model().objects.all()
        genres = Genre.objects.all()
        with open(file_path) as json_file:
            data = json.load(json_file)
            for book_data in data:
                author = Author.objects.create(
                    full_name=book_data['author'],
                    birthday=(book_data['year']-35)
                )
                Book.default_manager.create(
                    title=book_data['title'],
                    year=book_data['year'],
                    library=library,
                    author=author,
                    genre=random.choice(genres),
                    owner=random.choice(users)
                )

    def _fill_comments(self):
        users = get_user_model().objects.all()
        books = Book.default_manager.all()
        for book in books:
            for i in range(5):
                Comment.active.create(
                    book=book,
                    text=f'Содержательный комментарий о книге {book.title}',
                    owner=random.choice(users)
                )
