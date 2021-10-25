import pytest
from homework_drf.models import AnimeGenre


@pytest.mark.django_db
def test_genre_model_str_method():
    genre = AnimeGenre.objects.create(genre="someAnimeGenre")
    assert str(genre) == "someAnimeGenre"
