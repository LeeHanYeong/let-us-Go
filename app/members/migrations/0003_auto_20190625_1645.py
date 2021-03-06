# Generated by Django 2.2.2 on 2019-06-25 07:45

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0002_auto_20190621_1329"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", members.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name="user",
            name="birth_date",
        ),
        migrations.AddField(
            model_name="user",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="nickname",
            field=models.CharField(
                max_length=20, null=True, unique=True, verbose_name="닉네임"
            ),
        ),
    ]
