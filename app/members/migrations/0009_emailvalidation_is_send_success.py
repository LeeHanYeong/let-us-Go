# Generated by Django 2.2.2 on 2019-07-01 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_emailvalidation'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailvalidation',
            name='is_send_success',
            field=models.BooleanField(default=False),
        ),
    ]