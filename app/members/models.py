import string

from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django_aid.django.model import Manager
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from utils.models import DeleteModel

__all__ = (
    "User",
    "EmailVerification",
)


class UserManager(Manager, BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if extra_fields.get("type") == User.TYPE_EMAIL:
            username = email
        elif username is None:
            raise ValidationError("사용자 생성 필수값(username)이 주어지지 않았습니다")
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    TYPE_KAKAO, TYPE_FACEBOOK, TYPE_EMAIL = "kakao", "facebook", "email"
    TYPE_CHOICES = (
        (TYPE_KAKAO, "카카오"),
        (TYPE_FACEBOOK, "페이스북"),
        (TYPE_EMAIL, "이메일"),
    )
    first_name = None
    last_name = None
    name = models.CharField("이름", max_length=20, blank=True)
    type = models.CharField(
        "유형", max_length=10, choices=TYPE_CHOICES, default=TYPE_EMAIL
    )
    nickname = models.CharField(
        "닉네임", max_length=20, unique=True, blank=True, null=True
    )
    email = models.EmailField("이메일", unique=True)
    phone_number = PhoneNumberField("전화번호", blank=True)

    REQUIRED_FIELDS = ("email",)

    objects = UserManager()

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = f"{verbose_name} 목록"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.type == self.TYPE_EMAIL:
            self.username = self.email
        super().save(*args, **kwargs)


class EmailValidationManager(models.Manager):
    def create(self, **kwargs):
        instance, created = super().update_or_create(
            **kwargs,
            defaults={
                "status_verification": EmailVerification.WAIT,
                "status_send": EmailVerification.WAIT,
            },
        )
        if not created:
            instance.reset_code()
        return instance


class EmailVerification(TimeStampedModel):
    WAIT, SUCCEED, FAILED = "wait", "succeed", "failed"
    CHOICES_STATUS = (
        (WAIT, "대기"),
        (SUCCEED, "성공"),
        (FAILED, "실패"),
    )
    user = models.OneToOneField(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="email_verification",
        blank=True,
        null=True,
    )
    email = models.EmailField("이메일", unique=True)
    code = models.CharField("인증코드", max_length=50)

    status_verification = models.CharField(
        "인증상태", choices=CHOICES_STATUS, default=WAIT, max_length=10
    )
    status_send = models.CharField(
        "발송상태", choices=CHOICES_STATUS, default=WAIT, max_length=10
    )

    objects = EmailValidationManager()

    class Meta:
        verbose_name = "이메일 인증"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = ("-pk",)

    def __str__(self):
        return "{user}{email} (발송: {send}, 인증: {verification})".format(
            user=f"{self.user.name} | " if self.user else "",
            email=self.email,
            send=self.get_status_send_display(),
            verification=self.get_status_verification_display(),
        )

    def save(self, **kwargs):
        if not self.code:
            self.code = get_random_string(6, allowed_chars=string.digits)
        super().save(**kwargs)

    def reset_code(self):
        self.code = get_random_string(6, allowed_chars=string.digits)
        self.save()

    @property
    def is_verification_completed(self):
        return self.status_verification == self.SUCCEED

    @property
    def is_send_succeed(self):
        return self.status_send == self.SUCCEED
