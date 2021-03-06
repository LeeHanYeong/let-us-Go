# Generated by Django 2.2.2 on 2019-07-28 07:51

from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0014_session_weight"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpeakerLinkType",
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
                ("name", models.CharField(max_length=20, verbose_name="발표자 링크 유형")),
                (
                    "img_icon",
                    easy_thumbnails.fields.ThumbnailerField(
                        blank=True, upload_to="speaker/icon", verbose_name="링크 아이콘 이미지"
                    ),
                ),
            ],
            options={
                "verbose_name": "발표자 링크 유형",
                "verbose_name_plural": "발표자 링크 유형 목록",
            },
        ),
        migrations.AlterField(
            model_name="speaker",
            name="img_profile",
            field=easy_thumbnails.fields.ThumbnailerImageField(
                blank=True, upload_to="speaker", verbose_name="프로필 이미지"
            ),
        ),
        migrations.CreateModel(
            name="SpeakerLink",
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
                ("name", models.CharField(max_length=200, verbose_name="링크명")),
                (
                    "speaker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="link_set",
                        to="seminars.Speaker",
                        verbose_name="발표자",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="link_set",
                        to="seminars.SpeakerLinkType",
                        verbose_name="유형",
                    ),
                ),
            ],
            options={
                "verbose_name": "발표자 링크",
                "verbose_name_plural": "발표자 링크 목록",
            },
        ),
    ]
