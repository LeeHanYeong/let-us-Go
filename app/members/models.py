import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django_aid.django.model import Manager
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

__all__ = (
    "User",
    "EmailVerification",
)

from sentry_sdk import capture_exception

from utils.drf.exceptions import EmailSendFailed


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
    nickname = models.CharField("닉네임", max_length=20, blank=True)
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


class EmailVerificationManager(models.Manager):
    def create(self, **kwargs):
        instance, created = super().update_or_create(
            **kwargs,
            defaults={"status_send": EmailVerification.WAIT},
        )
        if not created:
            instance.reset_code()
        return instance


class EmailVerification(TimeStampedModel):
    TYPE_SIGNUP, TYPE_PASSWORD_RESET = "signup", "password_reset"
    CHOICES_TYPE = (
        (TYPE_SIGNUP, "회원가입 이메일 인증"),
        (TYPE_PASSWORD_RESET, "비밀번호 찾기 인증"),
    )
    WAIT, SUCCEED, FAILED = "wait", "succeed", "failed"
    CHOICES_STATUS = (
        (WAIT, "대기"),
        (SUCCEED, "성공"),
        (FAILED, "실패"),
    )
    type = models.CharField(
        "유형", choices=CHOICES_TYPE, default=TYPE_SIGNUP, max_length=20
    )
    user = models.OneToOneField(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="email_verification",
        blank=True,
        null=True,
    )
    email = models.EmailField("이메일")
    code = models.CharField("인증코드", max_length=50)
    status_send = models.CharField(
        "발송상태", choices=CHOICES_STATUS, default=WAIT, max_length=10
    )

    objects = EmailVerificationManager()

    class Meta:
        verbose_name = "이메일 인증"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = ("-pk",)
        indexes = [
            models.Index(fields=["type"]),
        ]

    def __str__(self):
        return "{user}{email} (발송: {send})".format(
            user=f"{self.user.name} | " if self.user else "",
            email=self.email,
            send=self.get_status_send_display(),
        )

    def save(self, **kwargs):
        if not self.code:
            self.code = get_random_string(6, allowed_chars=string.digits)
        super().save(**kwargs)

    def reset_code(self):
        self.code = get_random_string(6, allowed_chars=string.digits)
        self.save()

    def send(self):
        def _send_type_signup():
            subject = "let us: Go! 이메일 인증 코드 안내"
            result = send_mail(
                subject=subject,
                message=self.code,
                html_message=render_to_string(
                    template_name="members/email-validation.jinja2",
                    context={
                        "subject": subject,
                        "code": self.code,
                    },
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.email],
            )
            # 해당 이메일로 마지막으로 인증요청한 항목 외에 삭제
            EmailVerification.objects.filter(
                type=self.TYPE_SIGNUP, email=self.email
            ).exclude(id=self.id).delete()
            if result == 1:
                self.status_send = EmailVerification.SUCCEED
                self.save()
            elif result == 0:
                self.status_send = EmailVerification.FAILED
                self.save()
                e = EmailSendFailed(f"인증 이메일 발송에 실패했습니다({self.email})")
                capture_exception(e)
                raise e
            return result

        def _send_type_password_reset():
            subject = "let us: Go! 비밀번호 변경 코드"
            result = send_mail(
                subject=subject,
                message=self.code,
                html_message=render_to_string(
                    template_name="members/email-validation.jinja2",
                    context={
                        "subject": subject,
                        "code": self.code,
                    },
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.email],
            )
            # 해당 이메일로 마지막으로 인증요청한 항목 외에 삭제
            EmailVerification.objects.filter(
                type=self.TYPE_PASSWORD_RESET, email=self.email
            ).exclude(id=self.id).delete()
            if result == 1:
                self.status_send = EmailVerification.SUCCEED
                self.save()
            elif result == 0:
                self.status_send = EmailVerification.FAILED
                self.save()
                e = EmailSendFailed(f"인증 이메일 발송에 실패했습니다({self.email})")
                capture_exception(e)
                raise e
            return result

        type_function = {
            self.TYPE_SIGNUP: _send_type_signup,
            self.TYPE_PASSWORD_RESET: _send_type_password_reset,
        }
        with transaction.atomic():
            return type_function[self.type]()
