from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from utils.models import DeleteModel, DeleteModelManager


class UserManager(DeleteModelManager, BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if extra_fields.get('type') == User.TYPE_EMAIL:
            username = email
        elif username is None:
            raise ValidationError('사용자 생성 필수값(username)이 주어지지 않았습니다')
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel, DeleteModel):
    TYPE_KAKAO, TYPE_FACEBOOK, TYPE_EMAIL = 'kakao', 'facebook', 'email'
    TYPE_CHOICES = (
        (TYPE_KAKAO, '카카오'),
        (TYPE_FACEBOOK, '페이스북'),
        (TYPE_EMAIL, '이메일'),
    )
    first_name = None
    last_name = None
    name = models.CharField('이름', max_length=20, blank=True)
    type = models.CharField('유형', max_length=10, choices=TYPE_CHOICES, default=TYPE_EMAIL)
    nickname = models.CharField('닉네임', max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField('이메일', unique=True)
    phone_number = PhoneNumberField('전화번호', blank=True)

    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        if self.type == self.TYPE_EMAIL:
            self.username = self.email
        super().save(*args, **kwargs)

    def perform_delete(self):
        deleted_count = User.objects.filter(is_deleted=True).count()
        deleted_name = f'deleted_{deleted_count:05d}'
        self.username = deleted_name
        self.nickname = deleted_name
