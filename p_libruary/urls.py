from django.contrib import admin
from django.urls import path
from .views import book_decrement, book_increment, publishers, AuthorCreate, AuthorUpdate, AuthorList, PublisherDetailView, author_create_many, books_authors_create_many, friends_list, AuthorDelete
from django.conf import settings
from django.conf.urls.static import static

app_name = 'p_libruary'

urlpatterns = [
    path('index/book_increment/', book_increment),
    path('index/book_decrement/', book_decrement),
    path('publishers/', publishers),
    path('authors/create/', AuthorCreate.as_view(), name='author_create'),  
    path('authors/', AuthorList.as_view(), name='authors_list'),
    path('authors/<int:pk>/', AuthorUpdate.as_view(), name='author_edit'),
    path('authors/<int:pk>/delete/', AuthorDelete.as_view(), name='author_delete'),
    path('author/create_many/', author_create_many, name='author_create_many'),
    path('author_book/create_many/', books_authors_create_many, name='author_book_create_many'),
    path('friends/', friends_list),
]