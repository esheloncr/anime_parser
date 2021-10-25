import json
import pytest
from homework_drf.models import Anime, AnimeGenre
from django.urls import reverse
from rest_framework.test import APIClient


INDEX_URL = "http://127.0.0.1:8000/"


@pytest.fixture
def api_client():
    return APIClient()


def setup_model():
    first_genre = AnimeGenre.objects.create(genre="SomeTestGenre")
    second_genre = AnimeGenre.objects.create(genre="NewGenre")
    third_genre = AnimeGenre.objects.create(genre="RandomGenre")
    first_anime = Anime.objects.create(title="RandomAnime", episodes=55, rank="33")
    first_anime.genre.add(first_genre)
    first_anime.genre.add(third_genre)
    second_anime = Anime.objects.create(title="SecondAnime", episodes=33, rank="10")
    second_anime.genre.add(second_genre)
    second_anime.genre.add(first_genre)


@pytest.mark.django_db
def test_create_anime_error(api_client):
    data = {}
    response = api_client.post(
        f"{INDEX_URL}api/anime/", data=data, content_type="application/json"
    )
    assert response.status_code == 400
    assert response.data.get("error") == "No content in request"


@pytest.mark.django_db
def test_create_anime(api_client):
    genres = ["Action", "Fantasy", "Horror"]
    data = {
        "title": "SomeAnimeTitle",
        "episodes": 25,
        "rank": "10500",
        "genres": genres,
    }
    response = api_client.post(f"{INDEX_URL}api/anime/", data=data)
    assert response.status_code == 201
    assert response.data.get("message") == "created"
    assert len(AnimeGenre.objects.all()) == 3
    assert len(Anime.objects.all()) == 1
    obj = Anime.objects.first()
    assert obj.title == "SomeAnimeTitle"
    assert obj.episodes == 25
    assert obj.rank == "10500"
    assert len(obj.genre.all()) == len(AnimeGenre.objects.all())


@pytest.mark.django_db
def test_create_anime_without_genres(api_client):
    data = {"title": "SomeAnimeTitle", "episodes": 25, "rank": "10500"}
    response = api_client.post(f"{INDEX_URL}api/anime/", data=data)
    assert response.status_code == 201
    assert response.data.get("message") == "created"
    assert len(Anime.objects.all()) == 1
    assert not len(AnimeGenre.objects.all())


@pytest.mark.django_db
def test_anime_endpoint_extra_action_redirect(api_client):
    response = api_client.get(f"{INDEX_URL}api/anime/new/")
    assert response.status_code == 302
    assert len(Anime.objects.all()) == 1
