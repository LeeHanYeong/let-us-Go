# Generated by Django 2.2.2 on 2019-06-27 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0006_auto_20190627_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='attend_count',
            field=models.IntegerField(default=0, verbose_name='신청인원'),
        ),
        migrations.AddField(
            model_name='track',
            name='location',
            field=models.CharField(blank=True, max_length=100, verbose_name='장소'),
        ),
        migrations.AddField(
            model_name='track',
            name='total_attend_count',
            field=models.IntegerField(default=0, verbose_name='정원'),
        ),
    ]
