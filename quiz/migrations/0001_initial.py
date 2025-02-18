# Generated by Django 5.1.1 on 2024-09-06 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link", models.URLField()),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "cover_image",
                    models.ImageField(blank=True, null=True, upload_to="quiz_covers/"),
                ),
            ],
        ),
    ]
