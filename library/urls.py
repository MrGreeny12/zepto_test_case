from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from library.versions.v_1_0 import views

router = DefaultRouter()
router.register(r'books', views.BooksAPIViewSet, basename='books')
router.register(r'books/(?P<book_id>[^/.]+)/comments', views.CommentsAPIViewSet, basename='comments')
router.register(r'genres', views.GenreAPIViewSet, basename='genres')
router.register(r'authors', views.AuthorsAPIViewSet, basename='authors')

urlpatterns = [
    path('', include(router.urls)),
    path(r'api-token-auth/', obtain_auth_token, name='token_authentication_url')
]
