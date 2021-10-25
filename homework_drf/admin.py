from django.contrib import admin
from .models import Anime, AnimeGenre


class AnimeAdmin(admin.ModelAdmin):
    list_display = ["title", "episodes", "rank"]


class AdminGenre(admin.ModelAdmin):
    list_display = ["genre"]


admin.site.register(Anime, AnimeAdmin)
admin.site.register(AnimeGenre, AdminGenre)
