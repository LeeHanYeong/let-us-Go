# Generated by Django 3.1 on 2020-08-19 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0020_auto_20200814_0102"),
    ]

    operations = [
        migrations.CreateModel(
            name="SessionLinkCategory",
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
                ("name", models.CharField(max_length=100, verbose_name="세션 링크 타입")),
                (
                    "icon",
                    models.ImageField(
                        blank=True, upload_to="session/icon", verbose_name="아이콘 이미지"
                    ),
                ),
            ],
            options={
                "verbose_name": "세션 링크 타입",
                "verbose_name_plural": "세션 링크 타입 목록",
            },
        ),
        migrations.AddField(
            model_name="sessionlink",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="link_set",
                related_query_name="link",
                to="seminars.sessionlinkcategory",
                verbose_name="세션 링크 타입",
            ),
        ),
    ]
