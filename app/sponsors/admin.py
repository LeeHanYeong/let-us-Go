from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import SponsorTier, Sponsor


@admin.register(SponsorTier)
class SponsorTierAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_filter = ('seminar',)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier')
    list_filter = ('tier__seminar',)
