from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect
from .models import Book
from .anime_api import RandomAnimePicker, RandomAnimeFact
import json


def get_all_books(request) -> JsonResponse:
    """
    Get all books. If there no books return empty list
    :return: JSONResponse
    """
    queryset = Book.objects.all()
    serialized_data = []
    for obj in queryset:
        item = {"pk": obj.pk, "title": obj.title, "page_counter": obj.page_counter}
        serialized_data.append(item)
    return JsonResponse(serialized_data, safe=False)


@csrf_exempt
def get_book_by_pk(request, pk: int) -> JsonResponse:
    """
    This function trying to catch an object from DB by primary key.
    Allowed method: GET, PUT, DELETE
    :param request: WSGIRequest object
    :param pk: int primary key
    :return: JSONResponse
    """
    try:
        book = Book.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "not found"}, status="404")
    if request.method == "GET":
        serialized_data = {
            "pk": book.pk,
            "title": book.title,
            "page_counter": book.page_counter,
        }
        return JsonResponse(serialized_data)
    if request.method == "PUT":
        data = request.body.decode("utf-8")
        data = json.loads(data.replace("'", '"'))
        title = data.get("title")
        page_counter = data.get("page_counter")
        validated_data = validate((title, page_counter))
        if type(validated_data) is JsonResponse:
            return validated_data
        if book.title == title or book.page_counter == page_counter:
            return JsonResponse(
                {
                    "error": "The content of the field is the same as the current one. Use PATCH method "
                    "to change several fields"
                },
                status=400,
            )
        book.title = title
        book.page_counter = page_counter
        book.save()
        return JsonResponse({"message": "Book successfully updated"})
    if request.method == "DELETE":
        Book.objects.filter(pk=pk).delete()
        return JsonResponse({"message": "successfully deleted"}, status=200)
    if request.method == "POST":
        return JsonResponse({"error": "Method POST is not allowed"}, status=405)


def validate(data: tuple) -> JsonResponse:
    """
    Validate POST or PUT data and sends corresponding answer
    :param data: tuple of data by fields title and page_counter
    :return: JSONResponse
    """
    if not any(data):
        return JsonResponse(
            {"error": "fields 'title' and 'page_counter' are required"}, status="400"
        )
    if len(data) < 2:
        return JsonResponse(
            {"error": "Lost parameter 'title' or 'page_counter'"}, status=400
        )
    if not data[0]:
        return JsonResponse({"error": "field 'title' is required"}, status="400")
    if not data[1]:
        return JsonResponse({"error": "field 'page_counter' is required"}, status="400")
    try:
        int(data[1])
    except ValueError:
        return JsonResponse(
            {"error": "field 'page_counter' must be a number"}, status="400"
        )


@csrf_exempt
def create_book(request) -> JsonResponse:
    """
    Create new book object by POST request.
    :param request: WSGIRequest
    :return: JSONResponse
    """
    if request.method == "POST":
        data = request.POST
        title = data.get("title")
        page_counter = data.get("page_counter")
        validated_data = validate((title, page_counter))
        if type(validated_data) is JsonResponse:
            return validated_data
        new_book = Book.objects.create(title=title, page_counter=page_counter)
        new_book.save()
        return JsonResponse({"message": "book created"}, status="201")
    return redirect(reverse("all_books"))


def get_anime(request) -> JsonResponse:
    """
    That function call RandomAnimePicker and returns random parsed anime
    :request: WSGIRequest
    :return: JsonResponse
    """
    anime_picker = RandomAnimePicker()
    return JsonResponse(anime_picker.get_random_anime(), safe=False)


def get_anime_facts(request) -> JsonResponse:
    """
    That function calls RandomAnimeFact instance and return random facts in JSON
    :param request: WSGIRequest
    :return: JsonResponse
    """
    facts_picker = RandomAnimeFact()
    facts = facts_picker.get_random_facts()
    return JsonResponse(facts, safe=False)
