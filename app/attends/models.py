from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Attend(TimeStampedModel):
    STATUS_IN_PROGRESS, STATUS_SUCCEED, STATUS_FAILED = ('p', 'c', 'f')
    CHOICES_STATUS = (
        (STATUS_IN_PROGRESS, '처리중'),
        (STATUS_SUCCEED, '신청완료'),
        (STATUS_FAILED, '신청실패'),
    )
    TYPE_STUDENT, TYPE_NORMAL = ('s', 'n')
    CHOICES_TYPE = (
        (TYPE_STUDENT, '학생'),
        (TYPE_NORMAL, '일반'),
    )
    SIZE_S, SIZE_M, SIZE_L = ('s', 'm', 'l')
    CHOICES_SIZE = (
        (SIZE_S, 'S'),
        (SIZE_M, 'M'),
        (SIZE_L, 'L'),
    )
    is_canceled = models.BooleanField(default=False)
    status = models.CharField('상태', max_length=1, default=STATUS_IN_PROGRESS)
    seminar = models.ForeignKey(
        'seminars.Seminar', on_delete=models.CASCADE,
        verbose_name='세미나', related_name='attend_set',
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='사용자', related_name='attend_set',
    )
    name = models.CharField('이름(실명)', max_length=20)
    type = models.CharField('구분(학생/일반)', choices=CHOICES_TYPE, max_length=1)
    goods_size = models.CharField('굿즈 사이즈', choices=CHOICES_SIZE, blank=True, max_length=3)
    is_attend_after_party = models.BooleanField('뒷풀이 참석 여부')

    class Meta:
        verbose_name = '참가신청내역'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-created',)
        unique_together = (
            ('seminar', 'user'),
        )

    def __str__(self):
        return f'신청서 ({self.name})'
