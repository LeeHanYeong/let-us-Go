from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from markdownx.models import MarkdownxField

User = get_user_model()


class Seminar(TimeStampedModel):
    name = models.CharField('세미나명', max_length=100)
    start_at = models.DateTimeField('세미나 시작일시', blank=True, null=True, db_index=True)
    end_at = models.DateTimeField('세미나 종료일시', blank=True, null=True)
    address1 = models.CharField('주소', max_length=200, help_text='도로명/지번 주소')
    address2 = models.CharField('상세주소', max_length=100, help_text='건물명/층/호수/상세장소 등')

    entry_fee = models.PositiveIntegerField('참가비', blank=True, null=True)
    after_party_fee = models.PositiveIntegerField('회식비', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '세미나'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-start_at',)


class Session(TimeStampedModel):
    LEVEL_LOW, LEVEL_MID, LEVEL_HIGH = ('l', 'm', 'h')
    CHOICES_LEVEL = (
        (LEVEL_LOW, '초급'),
        (LEVEL_MID, '중급'),
        (LEVEL_HIGH, '고급'),
    )
    seminar = models.ForeignKey(
        'seminars.Seminar', on_delete=models.CASCADE,
        verbose_name='세미나', related_name='session_set',
    )
    level = models.CharField('레벨', choices=CHOICES_LEVEL, max_length=1, blank=True)
    name = models.CharField('세션명', max_length=50)
    short_description = models.CharField('세션 설명(간략)', max_length=200, blank=True)
    description = MarkdownxField('세션 설명', help_text='Markdown', blank=True)
    speaker = models.ForeignKey(
        User, verbose_name='발표자', on_delete=models.SET_NULL,
        related_name='session_set', blank=True, null=True,
    )
    speaker_alt_text = models.CharField(
        '발표자 대체 텍스트', max_length=50, help_text='발표자가 없는 세션의 경우 대체될 텍스트입니다',
    )
    start_time = models.TimeField('시작시간', blank=True, null=True)
    end_time = models.TimeField('종료시간', blank=True, null=True)

    def __str__(self):
        return f'{self.seminar.name} | {self.name}'

    class Meta:
        verbose_name = '세션'
        verbose_name_plural = f'{verbose_name} 목록'
