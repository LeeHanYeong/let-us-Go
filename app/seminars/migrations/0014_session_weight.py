# Generated by Django 2.2.2 on 2019-07-24 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0013_auto_20190724_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='weight',
            field=models.IntegerField(default=1, verbose_name='비중'),
        ),
    ]
