# Generated by Django 2.2.2 on 2021-10-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("homework_drf", "0002_auto_20211023_1326")]

    operations = [
        migrations.AlterField(
            model_name="anime",
            name="rank",
            field=models.CharField(max_length=255, verbose_name="Anime rating"),
        )
    ]