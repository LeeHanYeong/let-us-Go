# Generated by Django 2.2.2 on 2019-06-27 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0005_auto_20190626_1408"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="nickname",
            field=models.CharField(
                blank=True, max_length=20, null=True, unique=True, verbose_name="닉네임"
            ),
        ),
    ]
