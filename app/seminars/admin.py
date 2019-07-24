from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from markdownx.admin import MarkdownxModelAdmin

from .models import Seminar, Track, Session, Speaker, SessionVideo, SessionLink, SessionFile


class SessionVideoInline(admin.TabularInline):
    model = SessionVideo
    extra = 1


class SessionLinkInline(admin.TabularInline):
    model = SessionLink
    extra = 1


class SessionFileInline(admin.TabularInline):
    model = SessionFile
    extra = 1


@admin.register(SessionVideo)
class SessionVideoAdmin(admin.ModelAdmin):
    pass


@admin.register(SessionLink)
class SessionLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(SessionFile)
class SessionFileAdmin(admin.ModelAdmin):
    pass


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'seminar')
    list_filter = ('seminar',)
    readonly_fields = ('attend_count',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'track', 'start_time', 'end_time', 'weight')
    list_editable = ('weight',)
    list_filter = ('track',)
    inlines = [
        SessionVideoInline,
        SessionLinkInline,
        SessionFileInline,
    ]


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin_session_set',)

    def admin_session_set(self, obj):
        sessions = '\n'.join([
            f'<div>{str(session)}</div>' for session in obj.session_set.all()
        ])
        return format_html(f'<div>{sessions}</div>')

    admin_session_set.short_description = '발표한 세션 목록'
