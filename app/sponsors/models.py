from django.db import models
from django_extensions.db.models import TimeStampedModel


class Sponsor(TimeStampedModel):
    name = models.CharField('스폰서명', max_length=30)
    logo = models.ImageField('CI로고', upload_to='sponsors/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '스폰서'
        verbose_name_plural = f'{verbose_name} 목록'
