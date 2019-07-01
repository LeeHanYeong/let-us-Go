from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from markdownx.models import MarkdownxField
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Seminar(TimeStampedModel):
    name = models.CharField('세미나명', max_length=100)
    start_at = models.DateTimeField('세미나 시작일시', blank=True, null=True, db_index=True)
    end_at = models.DateTimeField('세미나 종료일시', blank=True, null=True)
    address1 = models.CharField('주소', max_length=200, help_text='도로명/지번 주소')
    address2 = models.CharField('상세주소', max_length=100, help_text='건물명/층/호수/상세장소 등')

    after_party_fee = models.PositiveIntegerField('회식비', blank=True, null=True)

    img_sponsors_web = models.ImageField('스폰서 이미지(웹)', upload_to='seminar', blank=True)
    img_sponsors_mobile = models.ImageField('스폰서 이미지(모바일)', upload_to='seminar', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '세미나'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-start_at',)


class Track(TimeStampedModel):
    seminar = models.ForeignKey(
        'seminars.Seminar', on_delete=models.CASCADE,
        verbose_name='세미나', related_name='track_set',
    )
    name = models.CharField('트랙명', max_length=100)
    location = models.CharField('장소', max_length=100, blank=True)
    total_attend_count = models.IntegerField('정원', default=0)
    attend_count = models.IntegerField('신청인원', default=0)

    entry_fee = models.PositiveIntegerField('참가비', blank=True, null=True)
    entry_fee_student = models.PositiveIntegerField('학생 참가비', blank=True, null=True)
    order = models.PositiveIntegerField('순서', default=0, blank=False, null=False)

    def __str__(self):
        return f'{self.seminar.name} | {self.name}'

    class Meta:
        verbose_name = '트랙'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('order',)


class Session(TimeStampedModel):
    LEVEL_LOW, LEVEL_MID, LEVEL_HIGH = ('low', 'mid', 'high')
    CHOICES_LEVEL = (
        (LEVEL_LOW, '초급'),
        (LEVEL_MID, '중급'),
        (LEVEL_HIGH, '고급'),
    )
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE,
        verbose_name='트랙', related_name='session_set',
    )
    level = models.CharField('레벨', choices=CHOICES_LEVEL, max_length=5, blank=True, db_index=True)
    name = models.CharField('세션명', max_length=50)
    short_description = models.CharField('세션 설명(간략)', max_length=200, blank=True)
    description = MarkdownxField('세션 설명', help_text='Markdown', blank=True)
    speaker = models.ForeignKey(
        'seminars.Speaker', verbose_name='발표자', on_delete=models.SET_NULL,
        related_name='session_set', blank=True, null=True, db_index=True,
    )
    speaker_alt_text = models.CharField(
        '발표자 대체 텍스트', max_length=50, help_text='발표자가 없는 세션의 경우 대체될 텍스트입니다', blank=True,
    )
    start_time = models.TimeField('시작시간', blank=True, null=True, db_index=True)
    end_time = models.TimeField('종료시간', blank=True, null=True, db_index=True)

    def __str__(self):
        return f'{self.track.seminar.name} | {self.track.name} | {self.name}'

    class Meta:
        verbose_name = '세션'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('-start_time',)


class Speaker(TimeStampedModel):
    name = models.CharField('이름', max_length=100, blank=True)
    email = models.EmailField('이메일', blank=True)
    phone_number = PhoneNumberField('전화번호', blank=True)
    img_profile = models.ImageField('프로필 이미지', upload_to='speaker', blank=True)

    facebook = models.CharField('Facebook 사용자명', max_length=100, blank=True)
    github = models.CharField('GitHub 사용자명', max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '스피커'
        verbose_name_plural = f'{verbose_name} 목록'
