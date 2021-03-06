# Generated by Django 2.2.2 on 2019-06-30 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0008_track_entry_fee_student"),
    ]

    operations = [
        migrations.AddField(
            model_name="seminar",
            name="img_sponsors_mobile",
            field=models.ImageField(
                blank=True, upload_to="seminar", verbose_name="스폰서 이미지(모바일)"
            ),
        ),
        migrations.AddField(
            model_name="seminar",
            name="img_sponsors_web",
            field=models.ImageField(
                blank=True, upload_to="seminar", verbose_name="스폰서 이미지(웹)"
            ),
        ),
    ]
