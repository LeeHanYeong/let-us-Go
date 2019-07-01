# Generated by Django 2.2.2 on 2019-07-01 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0009_auto_20190701_0256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ('-start_time',), 'verbose_name': '세션', 'verbose_name_plural': '세션 목록'},
        ),
        migrations.AlterField(
            model_name='session',
            name='end_time',
            field=models.TimeField(blank=True, db_index=True, null=True, verbose_name='종료시간'),
        ),
        migrations.AlterField(
            model_name='session',
            name='level',
            field=models.CharField(blank=True, choices=[('low', '초급'), ('mid', '중급'), ('high', '고급')], db_index=True, max_length=5, verbose_name='레벨'),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_time',
            field=models.TimeField(blank=True, db_index=True, null=True, verbose_name='시작시간'),
        ),
    ]
