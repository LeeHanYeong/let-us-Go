# Generated by Django 3.1 on 2020-08-24 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0013_remove_user_is_deleted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="emailverification",
            name="status_verification",
        ),
    ]
