from django.db import models
from django_extensions.db.models import TimeStampedModel

from seminars.models import Seminar


class SponsorTier(models.Model):
    seminar = models.ForeignKey(
        Seminar,
        verbose_name="세미나",
        related_name="sponsor_tier_set",
        on_delete=models.CASCADE,
    )
    name = models.CharField("등급명", max_length=20, blank=True)
    order = models.PositiveIntegerField("순서", default=0, blank=False, null=False)

    class Meta:
        verbose_name = "스폰서 등급"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = ("order",)

    def __str__(self):
        return "{seminar} | {tier_name} ({order})".format(
            seminar=self.seminar.name, tier_name=self.name, order=self.order,
        )


class Sponsor(TimeStampedModel):
    tier = models.ForeignKey(
        SponsorTier,
        verbose_name="등급",
        null=True,
        related_name="sponsor_set",
        on_delete=models.CASCADE,
    )
    name = models.CharField("스폰서명", max_length=30)
    logo = models.FileField("CI로고", upload_to="sponsors", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "스폰서"
        verbose_name_plural = f"{verbose_name} 목록"
        ordering = (
            "tier__seminar",
            "tier__order",
        )
