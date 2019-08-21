from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from easy_thumbnails.fields import ThumbnailerImageField, ThumbnailerField
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


class SessionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'speaker',
        ).prefetch_related(
            'speaker__link_set',
            'speaker__link_set__type',
        )


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
    description = models.TextField('세션 설명', blank=True)
    speaker = models.ForeignKey(
        'seminars.Speaker', verbose_name='발표자', on_delete=models.SET_NULL,
        related_name='session_set', blank=True, null=True, db_index=True,
    )
    speaker_alt_text = models.CharField(
        '발표자 대체 텍스트', max_length=50, help_text='발표자가 없는 세션의 경우 대체될 텍스트입니다', blank=True,
    )
    start_time = models.TimeField('시작시간', blank=True, null=True, db_index=True)
    end_time = models.TimeField('종료시간', blank=True, null=True, db_index=True)

    weight = models.IntegerField('비중', default=1)

    objects = SessionManager()

    def __str__(self):
        return f'{self.track.seminar.name} | {self.track.name} | {self.name}'

    class Meta:
        verbose_name = '세션'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ('start_time',)


class SessionVideo(models.Model):
    TYPE_LINK, TYPE_YOUTUBE = 'link', 'youtube'
    CHOICES_TYPE = (
        (TYPE_LINK, '링크'),
        (TYPE_YOUTUBE, 'YouTube'),
    )
    session = models.ForeignKey(
        Session, verbose_name='세션',
        related_name='video_set', on_delete=models.CASCADE,
    )
    type = models.CharField('유형', default=TYPE_LINK, choices=CHOICES_TYPE, max_length=12)
    name = models.CharField('영상명', max_length=100)
    key = models.CharField('영상 UniqueID', blank=True, max_length=100)
    url = models.URLField('영상 URL', blank=True)

    class Meta:
        verbose_name = '세션 영상'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.key and self.url:
            raise ValueError('영상의 ID또는 URL중 하나만 입력되어야 합니다')
        if self.type != self.TYPE_LINK and self.url:
            raise ValueError('링크가 아닌 유형의 경우에는 key만 허용됩니다')
        super().save(*args, **kwargs)


class SessionLink(models.Model):
    session = models.ForeignKey(
        Session, verbose_name='세션',
        related_name='link_set', on_delete=models.CASCADE,
    )
    name = models.CharField('링크명', max_length=100)
    url = models.URLField('URL', blank=True)

    class Meta:
        verbose_name = '세션 링크'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


class SessionFile(models.Model):
    session = models.ForeignKey(
        Session, verbose_name='세션',
        related_name='file_set', on_delete=models.CASCADE,
    )
    name = models.CharField('파일명', max_length=100)
    attachment = models.FileField('첨부파일', upload_to='session', blank=True)

    class Meta:
        verbose_name = '세션 첨부파일'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


class SpeakerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'link_set',
        )


class Speaker(TimeStampedModel):
    name = models.CharField('이름', max_length=100, blank=True)
    email = models.EmailField('이메일', blank=True)
    phone_number = PhoneNumberField('전화번호', blank=True)
    img_profile = ThumbnailerImageField('프로필 이미지', upload_to='speaker', blank=True)

    facebook = models.CharField('Facebook 사용자명', max_length=100, blank=True)
    github = models.CharField('GitHub 사용자명', max_length=100, blank=True)

    objects = SpeakerManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '스피커'
        verbose_name_plural = f'{verbose_name} 목록'


class SpeakerLinkType(models.Model):
    name = models.CharField('발표자 링크 유형', max_length=20)
    img_icon = ThumbnailerField('링크 아이콘 이미지', upload_to='speaker/icon', blank=True)

    class Meta:
        verbose_name = '발표자 링크 유형'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name


class SpeakerLink(models.Model):
    speaker = models.ForeignKey(
        Speaker, on_delete=models.CASCADE,
        related_name='link_set', verbose_name='발표자',
    )
    type = models.ForeignKey(
        SpeakerLinkType, on_delete=models.SET_NULL,
        related_name='link_set', verbose_name='유형', blank=True, null=True,
    )
    name = models.CharField('링크명', max_length=200)
    url = models.URLField('URL', blank=True)

    class Meta:
        verbose_name = '발표자 링크'
        verbose_name_plural = f'{verbose_name} 목록'

    def __str__(self):
        return self.name
