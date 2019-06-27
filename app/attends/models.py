from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Attend(TimeStampedModel):
    STATUS_IN_PROGRESS, STATUS_SUCCEED, STATUS_FAILED = ('in_progress', 'succeed', 'failed')
    CHOICES_STATUS = (
        (STATUS_IN_PROGRESS, '처리중'),
        (STATUS_SUCCEED, '신청완료'),
        (STATUS_FAILED, '신청실패'),
    )
    APPLICANT_TYPE_NORMAL, APPLICANT_TYPE_STAFF = ('normal', 'staff')
    CHOICES_APPLICANT_TYPE = (
        (APPLICANT_TYPE_NORMAL, '일반'),
        (APPLICANT_TYPE_STAFF, '스태프'),
    )
    DISCOUNT_TYPE_NORMAL, DISCOUNT_TYPE_STUDENT = ('normal', 'student')
    CHOICES_DISCOUNT_TYPE = (
        (DISCOUNT_TYPE_NORMAL, '일반'),
        (DISCOUNT_TYPE_STUDENT, '학생'),
    )
    SIZE_S, SIZE_M, SIZE_L = ('s', 'm', 'l')
    CHOICES_SIZE = (
        (SIZE_S, 'S'),
        (SIZE_M, 'M'),
        (SIZE_L, 'L'),
    )
    is_canceled = models.BooleanField(default=False)

    status = models.CharField('상태', max_length=12, default=STATUS_IN_PROGRESS, db_index=True)
    track = models.ForeignKey(
        'seminars.Track', on_delete=models.CASCADE,
        verbose_name='트랙', related_name='attend_set',
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='사용자', related_name='attend_set',
    )
    name = models.CharField('이름(실명)', max_length=20, db_index=True)
    applicant_type = models.CharField(
        '지원자 구분', choices=CHOICES_APPLICANT_TYPE,
        default=APPLICANT_TYPE_NORMAL, max_length=10, db_index=True)
    discount_type = models.CharField(
        '할인 구분', choices=CHOICES_DISCOUNT_TYPE,
        default=DISCOUNT_TYPE_NORMAL, max_length=10, db_index=True)
    goods_size = models.CharField('굿즈 사이즈', choices=CHOICES_SIZE, blank=True, max_length=3)
    is_attend_after_party = models.BooleanField('뒷풀이 참석 여부', db_index=True)

    class Meta:
        verbose_name = '참가신청내역'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-created',)
        unique_together = (
            ('track', 'user'),
        )

    def __str__(self):
        return f'신청서 ({self.name})'
