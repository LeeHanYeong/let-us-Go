# Generated by Django 2.2.2 on 2019-06-25 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attends", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="attend",
            old_name="attend_after_party",
            new_name="is_attend_after_party",
        ),
        migrations.AddField(
            model_name="attend",
            name="status",
            field=models.CharField(default="p", max_length=1, verbose_name="상태"),
        ),
    ]
