from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'nickname', 'type')
    list_filter = ('is_staff', 'groups')
    fieldsets = (
        (None, {
            'fields': (
                'username', 'type', 'password',
            )
        }),
        ('개인정보', {
            'fields': (
                'first_name', 'last_name', 'phone_number',
            )
        }),
        ('권한', {
            'fields': (
                'groups',
            )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
            )
        }),
        ('개인정보', {
            'fields': (
                'first_name', 'last_name', 'phone_number', 'birth_date',
            )
        })
    )
