# Generated by Django 3.1 on 2020-09-01 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0017_auto_20200831_2224"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailverification",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="이메일"),
        ),
    ]
