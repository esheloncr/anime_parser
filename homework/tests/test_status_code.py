import pytest


INDEX_URL = "http://127.0.0.1:8000"


@pytest.mark.django_db
def test_books_status_code(client):
    response = client.get(f"{INDEX_URL}/books")
    assert response.status_code == 200


@pytest.mark.django_db
def test_books_status_code_post(client):
    response = client.post(f"{INDEX_URL}/books/", {})
    assert response.status_code == 400


@pytest.mark.django_db
def test_anime_status_code(client):
    response = client.get(f"{INDEX_URL}/books")
    assert response.status_code == 200


@pytest.mark.django_db
def test_anime_facts_status_code(client):
    response = client.get(f"{INDEX_URL}/books")
    assert response.status_code == 200
