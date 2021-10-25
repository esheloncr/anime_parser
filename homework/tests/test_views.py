import pytest
import json
from homework.views import validate
from rest_framework.test import APIClient
from django.urls import reverse
from django.http import JsonResponse
from homework.models import Book


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_anime_facts(api_client):
    response = api_client.get(reverse("random_fact"))
    assert response.status_code == 200
    data = json.loads(response.content)
    anime_title = data.pop("anime")
    assert type(anime_title) is str
    facts = data.pop("facts")
    assert type(facts) is list
    for fact in facts:
        assert type(fact) is str


@pytest.mark.django_db
def test_get_anime(api_client):
    response = api_client.get(reverse("anime"))
    assert response.status_code == 200
    data = json.loads(response.content)
    assert type(data) is dict
    assert type(data.get("title")) is str
    assert type(data.get("episodes")) is int
    assert type(data.get("genres")) and type(data.get("pictures")) is list
    assert type(data.get("rank")) is int or type(data.get("rank")) is str


@pytest.mark.django_db
def test_create_book(api_client):
    data = {"title": "Some test book", "page_counter": 5}
    response = api_client.post(reverse("new_book"), data=data)
    assert response.status_code == 201


def check_wrong_json_response(response) -> bool:
    assert type(response) is JsonResponse
    assert response.status_code == 400
    return True


def setup_model() -> None:
    Book.objects.create(title="some text", page_counter=3)
    Book.objects.create(title="second text", page_counter=2)
    Book.objects.create(title="zxc", page_counter=55)


@pytest.mark.django_db
def test_validate_function(api_client):
    title = "Some text"
    page_counter = "12"
    validated_data = validate((title, page_counter))
    assert not validated_data
    validated_data = validate((title,))
    assert check_wrong_json_response(validated_data)
    assert (
        json.loads(validated_data.content).get("error")
        == "Lost parameter 'title' or 'page_counter'"
    )
    validated_data = validate(())
    assert check_wrong_json_response(validated_data)
    assert (
        json.loads(validated_data.content).get("error")
        == "fields 'title' and 'page_counter' are required"
    )
    validated_data = validate((None, 55))
    assert check_wrong_json_response(validated_data)
    assert (
        json.loads(validated_data.content).get("error") == "field 'title' is required"
    )
    validated_data = validate((title, None))
    assert check_wrong_json_response(validated_data)
    assert (
        json.loads(validated_data.content).get("error")
        == "field 'page_counter' is required"
    )
    validated_data = validate((title, title))
    assert check_wrong_json_response(validated_data)
    assert (
        json.loads(validated_data.content).get("error")
        == "field 'page_counter' must be a number"
    )


@pytest.mark.django_db
def test_create_book_redirect(api_client):
    response = api_client.get(reverse("new_book"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_book_by_pk_get(api_client):
    setup_model()
    for i in range(1, 3):
        response = api_client.get(reverse("book_by_pk", args=(i,)))
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3


@pytest.mark.django_db
def test_get_book_by_pk_put(api_client):
    setup_model()
    data = {"title": "Something New", "page_counter": 5}
    response = api_client.put(
        reverse("book_by_pk", args=(1,)), data, content_type="application/json"
    )
    assert response.status_code == 200
    assert json.loads(response.content).get("message") == "Book successfully updated"
    assert Book.objects.get(pk=1).title == "Something New"
    assert Book.objects.get(pk=1).page_counter == 5


@pytest.mark.django_db
def test_get_book_by_pk_delete_post(api_client):
    setup_model()
    response = api_client.delete(reverse("book_by_pk", args=(1,)))
    assert response.status_code == 200
    assert json.loads(response.content).get("message") == "successfully deleted"
    assert len(Book.objects.all()) == 2
    assert api_client.delete(reverse("book_by_pk", args=(1,))).status_code == 404
    response = api_client.post(reverse("book_by_pk", args=(2,)))
    assert response.status_code == 405


@pytest.mark.django_db
def test_get_book_by_pk_put_return_error(api_client):
    Book.objects.create(title="TestTitle", page_counter=2)
    response = api_client.put(
        reverse("book_by_pk", args=(1,)),
        {"title": 5, "page_counter": "text"},
        content_type="application/json",
    )
    assert response.status_code == 400
    assert (
        json.loads(response.content).get("error")
        == "field 'page_counter' must be a number"
    )


@pytest.mark.django_db
def test_get_book_by_pk_put_same_data(api_client):
    Book.objects.create(title="TestTitle", page_counter=2)
    response = api_client.put(
        reverse("book_by_pk", args=(1,)),
        {"title": "New title", "page_counter": 2},
        content_type="application/json",
    )
    assert response.status_code == 400
    assert (
        json.loads(response.content).get("error")
        == "The content of the field is the same as the current one. "
        "Use PATCH method to change several fields"
    )


@pytest.mark.django_db
def test_get_all_book(api_client):
    setup_model()
    response = api_client.get(reverse("all_books"))
    assert response.status_code == 200
    data = json.loads(response.content)
    assert len(data) == 3
    for item in data:
        assert type(item.get("pk")) and type(item.get("page_counter")) is int
        assert len(item.get("title")) > 1
