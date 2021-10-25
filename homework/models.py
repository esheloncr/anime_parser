from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Book name")
    page_counter = models.PositiveIntegerField(verbose_name="Number of pages")

    class Meta:
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title
