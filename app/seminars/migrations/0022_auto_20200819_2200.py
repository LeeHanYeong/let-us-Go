# Generated by Django 3.1 on 2020-08-19 13:00

from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0021_auto_20200819_2150"),
    ]

    operations = [
        migrations.CreateModel(
            name="SessionLinkType",
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
                        blank=True, upload_to="session/icon", verbose_name="링크 아이콘 이미지"
                    ),
                ),
            ],
            options={
                "verbose_name": "세션 링크 유형",
                "verbose_name_plural": "세션 링크 유형 목록",
            },
        ),
        migrations.RemoveField(
            model_name="sessionlink",
            name="category",
        ),
        migrations.AlterField(
            model_name="sessionlink",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="link_set",
                related_query_name="link",
                to="seminars.session",
                verbose_name="세션",
            ),
        ),
        migrations.DeleteModel(
            name="SessionLinkCategory",
        ),
        migrations.AddField(
            model_name="sessionlink",
            name="type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="link_set",
                related_query_name="link",
                to="seminars.sessionlinktype",
                verbose_name="세션 링크 유형",
            ),
        ),
    ]
