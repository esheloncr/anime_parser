from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
from .views import (
    get_all_books,
    get_book_by_pk,
    create_book,
    get_anime,
    get_anime_facts,
)

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("books", get_all_books, name="all_books"),
    path("books/<int:pk>", get_book_by_pk, name="book_by_pk"),
    path("books/", create_book, name="new_book"),
    path("anime", get_anime, name="anime"),
    path("anime-facts", get_anime_facts, name="random_fact"),
    path("api/", include("homework_drf.api.v1.urls")),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
