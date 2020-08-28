# Generated by Django 2.2.2 on 2019-07-01 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0011_auto_20190701_1502"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="emailverification",
            options={
                "ordering": ("-pk",),
                "verbose_name": "이메일 인증",
                "verbose_name_plural": "이메일 인증 목록",
            },
        ),
        migrations.RemoveField(
            model_name="emailverification",
            name="is_send_succeed",
        ),
        migrations.RemoveField(
            model_name="emailverification",
            name="is_verification_completed",
        ),
        migrations.AddField(
            model_name="emailverification",
            name="status_send",
            field=models.CharField(
                choices=[("wait", "대기"), ("succeed", "성공"), ("failed", "실패")],
                default="wait",
                max_length=10,
                verbose_name="발송상태",
            ),
        ),
        migrations.AddField(
            model_name="emailverification",
            name="status_verification",
            field=models.CharField(
                choices=[("wait", "대기"), ("succeed", "성공"), ("failed", "실패")],
                default="wait",
                max_length=10,
                verbose_name="인증상태",
            ),
        ),
    ]
