# Generated by Django 2.2.2 on 2019-06-21 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="seminar",
            options={
                "ordering": ("-start_at",),
                "verbose_name": "세미나",
                "verbose_name_plural": "세미나 목록",
            },
        ),
        migrations.AlterModelOptions(
            name="session",
            options={"verbose_name": "세션", "verbose_name_plural": "세션 목록"},
        ),
        migrations.AlterField(
            model_name="seminar",
            name="start_at",
            field=models.DateTimeField(
                blank=True, db_index=True, null=True, verbose_name="세미나 시작일시"
            ),
        ),
    ]
