# Generated by Django 2.2.2 on 2019-06-25 09:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0002_auto_20190621_1329'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attends', '0002_auto_20190625_1836'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attend',
            unique_together={('seminar', 'user')},
        ),
    ]