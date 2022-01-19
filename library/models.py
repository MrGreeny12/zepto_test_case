from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Library(models.Model):
    '''
    Модель библиотеки
    '''
    title = models.CharField(max_length=512, verbose_name='Название')
    address = models.CharField(max_length=2048, verbose_name='Адрес')
    working_hours = models.CharField(max_length=512, verbose_name='Часы работы',
                                     help_text='Указывайте часы в формате %H:%M - %H:%M')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Библиотека'
        verbose_name_plural = 'Список библиотек'
        db_table = 'libraries'
        indexes = [
            models.Index(fields=['title'])
        ]


class Genre(models.Model):
    '''
    Модель жанра книги
    '''
    title = models.CharField(max_length=512, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        db_table = 'genres'


class Author(models.Model):
    '''
    Модель автора книги
    '''
    full_name = models.CharField(max_length=512, verbose_name='ФИО')
    birthday = models.IntegerField(validators=[MaxValueValidator(2022), MinValueValidator(0)],
                                   verbose_name='Год рождения')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        db_table = 'authors'


class Book(models.Model):
    '''
    Модель книги
    '''
    title = models.CharField(max_length=512, verbose_name='Название')
    year = models.IntegerField(validators=[MaxValueValidator(2022), MinValueValidator(0)], blank=True, null=True,
                               verbose_name='Год выпуска')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='Автор'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='books',
        null=True,
        verbose_name='Жанр'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        db_table = 'books'
        indexes = [
            models.Index(fields=['title'])
        ]


class Comment(models.Model):
    '''
    Модель комментария для книги
    '''
    commenter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Книга'
    )
    text = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Комментарий {self.commenter.username}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии к книгам'
        db_table = 'comments'
        indexes = [
            models.Index(fields=['book'])
        ]
