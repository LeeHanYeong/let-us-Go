# Generated by Django 2.2.2 on 2019-07-24 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0013_auto_20190724_2131'),
        ('sponsors', '0002_auto_20190627_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, verbose_name='등급명')),
                ('seminar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsor_tier_set', to='seminars.Seminar', verbose_name='세미나')),
            ],
        ),
        migrations.AddField(
            model_name='sponsor',
            name='tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsor_set', to='sponsors.SponsorTier', verbose_name='등급'),
        ),
    ]
