from django.db import models


class Anime(models.Model):
    title = models.CharField(max_length=255, verbose_name="Anime title")
    episodes = models.PositiveIntegerField()
    rank = models.CharField(max_length=255, verbose_name="Anime rating")
    genre = models.ManyToManyField(
        "AnimeGenre",
        verbose_name="Genres",
        related_name="anime_rel",
        null=True,
        blank=True,
    )


class AnimeGenre(models.Model):
    genre = models.CharField(verbose_name="Anime genre", max_length=255)

    def __str__(self):
        return self.genre
