from django.contrib import admin
from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails.widgets import ImageClearableFileInput


class ThumbnailAdminMixin(admin.ModelAdmin):
    formfield_overrides = {
        ThumbnailerField: {
            "widget": ImageClearableFileInput,
        }
    }
