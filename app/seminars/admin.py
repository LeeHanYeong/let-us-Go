from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Seminar, Track, Session, Speaker


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(MarkdownxModelAdmin):
    pass


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    pass
