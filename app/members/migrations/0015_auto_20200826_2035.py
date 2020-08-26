# Generated by Django 3.1 on 2020-08-26 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0014_remove_emailverification_status_verification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="nickname",
            field=models.CharField(
                blank=True, default="", max_length=20, verbose_name="닉네임"
            ),
            preserve_default=False,
        ),
    ]
