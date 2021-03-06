# Generated by Django 2.2.2 on 2019-07-28 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sponsors", "0005_auto_20190724_2157"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sponsor",
            options={
                "ordering": ("tier__seminar", "tier__order"),
                "verbose_name": "스폰서",
                "verbose_name_plural": "스폰서 목록",
            },
        ),
        migrations.AlterField(
            model_name="sponsor",
            name="logo",
            field=models.FileField(
                blank=True, upload_to="sponsors", verbose_name="CI로고"
            ),
        ),
    ]
