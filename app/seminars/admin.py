from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Seminar
from .models import Session


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(MarkdownxModelAdmin):
    pass
