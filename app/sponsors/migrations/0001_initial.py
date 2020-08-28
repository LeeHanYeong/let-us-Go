# Generated by Django 2.2.2 on 2019-06-21 04:29

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sponsor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="스폰서명")),
                (
                    "logo",
                    models.ImageField(
                        blank=True, upload_to="sponsors/", verbose_name="CI로고"
                    ),
                ),
            ],
            options={
                "verbose_name": "스폰서",
                "verbose_name_plural": "스폰서 목록",
            },
        ),
    ]
