from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    TYPE_KAKAO, TYPE_FACEBOOK, TYPE_EMAIL = 'kakao', 'facebook', 'email'
    TYPE_CHOICES = (
        (TYPE_KAKAO, '카카오'),
        (TYPE_FACEBOOK, '페이스북'),
        (TYPE_EMAIL, '이메일'),
    )
    type = models.CharField('유형', max_length=10, choices=TYPE_CHOICES, default=TYPE_EMAIL)
    phone_number = PhoneNumberField('전화번호', blank=True)
    birth_date = models.DateField('생년월일', blank=True, null=True)
