from django.db import models
from django.db.models import QuerySet


class CommentManager(models.Manager):

    def get_book_comments(self, book_id: int) -> QuerySet:
        return self.filter(book__id=book_id)
