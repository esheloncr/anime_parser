from rest_framework import serializers
from homework_drf.models import Anime, AnimeGenre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeGenre
        fields = "__all__"


class AnimeSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        fields = ["title", "episodes", "rank", "genre"]
