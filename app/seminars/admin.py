from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html

from utils.django.admin import ThumbnailAdminMixin
from .models import Seminar, Track, Session, Speaker, SessionVideo, SessionLink, SessionFile, SpeakerLinkType, \
    SpeakerLink


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
    list_display = ('admin_description',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'track_set',
            'track_set__session_set',
        )

    def admin_description(self, obj):
        return format_html(render_to_string('admin/seminars/seminar_description.jinja2', {
            'seminar': obj,
        }))

    admin_description.short_description = '세미나'


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


class SpeakerLinkInline(admin.TabularInline):
    model = SpeakerLink
    extra = 1


@admin.register(Speaker)
class SpeakerAdmin(ThumbnailAdminMixin):
    list_display = (
        'name',
        'img_profile_thumbnail',
        'admin_session_set',
        'admin_link_set',
    )
    inlines = [
        SpeakerLinkInline,
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'session_set',
            'session_set__track',
            'session_set__track__seminar',
        )

    def img_profile_thumbnail(self, obj):
        return render_to_string('admin/thumbnail.html', {
            'image': obj.img_profile,
        })

    def admin_session_set(self, obj):
        sessions = '\n'.join([
            f'<div>{str(session)}</div>' for session in obj.session_set.all()
        ])
        return format_html(f'<div>{sessions}</div>')

    def admin_link_set(self, obj):
        links = '\n'.join([
            f'<li><a href="{link.url}">{link.name}</a></li>' for link in obj.link_set.all()
        ])
        return format_html(f'<ul>{links}</ul>')

    img_profile_thumbnail.short_description = '프로필 이미지'
    admin_session_set.short_description = '발표한 세션 목록'
    admin_link_set.short_description = '링크 목록'


@admin.register(SpeakerLinkType)
class SpeakerLinkTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(SpeakerLink)
class SpeakerLinkAdmin(admin.ModelAdmin):
    pass
