import pytest
from homework.models import Book


@pytest.mark.django_db
def test_create_model():
    book = Book.objects.create(title="Some test book", page_counter=6)
    assert len(Book.objects.all()) is 1
    assert str(book) is "Some test book"


@pytest.mark.django_db
def test_create_model_errors():
    with pytest.raises(ValueError):
        book = Book.objects.create(title=None, page_counter="Some string to test")
