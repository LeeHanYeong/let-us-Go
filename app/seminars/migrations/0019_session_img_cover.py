# Generated by Django 2.2.2 on 2019-09-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0018_auto_20190913_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='img_cover',
            field=models.ImageField(blank=True, upload_to='session', verbose_name='커버이미지'),
        ),
    ]
