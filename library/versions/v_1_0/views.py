from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from library.models import Book, Genre, Comment, Author
from library.permissions import IsOwnerOrReadOnly
from library.versions.v_1_0.serializers import BookSerializer, GenreSerializer, CommentSerializer, AuthorSerializer


class BooksAPIViewSet(viewsets.ModelViewSet):
    '''
    Представление (v. 1.0) для модели книг
    '''
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Book.default_manager.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GenreAPIViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    Представление (v. 1.0) для модели жанров
    '''
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()
    lookup_field = 'id'


class CommentsAPIViewSet(viewsets.ModelViewSet):
    '''
    Представление (v. 1.0) для модели комментариев
    '''
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        return Comment.active.get_book_comments(book_id=self.kwargs['book_id'])

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AuthorsAPIViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    Представление (v. 1.0) для модели авторов
    '''
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
