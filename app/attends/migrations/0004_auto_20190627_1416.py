# Generated by Django 2.2.2 on 2019-06-27 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attends", "0003_auto_20190625_1837"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attend",
            name="type",
        ),
        migrations.AddField(
            model_name="attend",
            name="applicant_type",
            field=models.CharField(
                choices=[("n", "일반"), ("s", "스태프")],
                db_index=True,
                default="n",
                max_length=1,
                verbose_name="지원자 구분",
            ),
        ),
        migrations.AddField(
            model_name="attend",
            name="discount_type",
            field=models.CharField(
                choices=[("n", "일반"), ("s", "학생")],
                db_index=True,
                default="n",
                max_length=1,
                verbose_name="할인 구분",
            ),
        ),
        migrations.AlterField(
            model_name="attend",
            name="is_attend_after_party",
            field=models.BooleanField(db_index=True, verbose_name="뒷풀이 참석 여부"),
        ),
        migrations.AlterField(
            model_name="attend",
            name="name",
            field=models.CharField(db_index=True, max_length=20, verbose_name="이름(실명)"),
        ),
        migrations.AlterField(
            model_name="attend",
            name="status",
            field=models.CharField(
                db_index=True, default="p", max_length=1, verbose_name="상태"
            ),
        ),
    ]
