# Generated by Django 2.2.2 on 2019-06-27 05:16

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0002_auto_20190621_1329"),
    ]

    operations = [
        migrations.CreateModel(
            name="Speaker",
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
                (
                    "name",
                    models.CharField(blank=True, max_length=100, verbose_name="이름"),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="이메일"),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, region=None, verbose_name="전화번호"
                    ),
                ),
                (
                    "facebook",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Facebook 사용자명"
                    ),
                ),
                (
                    "github",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="GitHub 사용자명"
                    ),
                ),
            ],
            options={
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="session",
            name="seminar",
        ),
        migrations.CreateModel(
            name="Track",
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
                ("name", models.CharField(max_length=100, verbose_name="트랙명")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="순서")),
                (
                    "seminar",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="track_set",
                        to="seminars.Seminar",
                        verbose_name="세미나",
                    ),
                ),
            ],
            options={
                "verbose_name": "트랙",
                "verbose_name_plural": "트랙 목록",
            },
        ),
        migrations.AddField(
            model_name="session",
            name="track",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="session_set",
                to="seminars.Track",
                verbose_name="트랙",
            ),
            preserve_default=False,
        ),
    ]
