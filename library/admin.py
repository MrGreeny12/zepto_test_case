from django.contrib import admin

from library.models import Library, Author, Book, Genre, Comment

admin.site.register(Library)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Comment)
