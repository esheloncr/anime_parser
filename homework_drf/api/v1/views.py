from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from homework_drf.models import Anime, AnimeGenre
from .serializers import AnimeSerializer, GenreSerializer
from homework.anime_api import RandomAnimePicker


class AnimeAPIView(ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    anime_picker = RandomAnimePicker()

    def create(self, request, *args, **kwargs):
        genres = request.POST.getlist("genres")
        if not len(request.data):
            return Response(
                {"error": "No content in request"}, status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        self._create_genres(genres, obj)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "created"}, status=status.HTTP_201_CREATED, headers=headers
        )

    def _create_genres(self, genres: str, obj):
        if not len(genres):
            return
        for genre in genres:
            new_genre = AnimeGenre.objects.get_or_create(
                genre=genre, defaults={"genre": genre}
            )
            new_genre[0].save()
            obj.genre.add(new_genre[0])

    @action(methods=["GET"], detail=False, url_path="new")
    def new(self, request):
        data = self.anime_picker.get_random_anime()
        genres = data.pop("genres")
        data.pop("pictures")
        new_obj = self.queryset.create(**data)
        new_obj.save()
        self._create_genres(genres, new_obj)
        return redirect("../")


class GenreAPIView(ModelViewSet):
    queryset = AnimeGenre.objects.all()
    serializer_class = GenreSerializer
