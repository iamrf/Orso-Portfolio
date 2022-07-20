from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from .models import *

@admin.register(Image)
class ImageAdmin(ModelAdminJalaliMixin , admin.ModelAdmin):
    list_display = ['name', 'admin_thumbnail']


admin.site.register(ImageAlbum)
admin.site.register(VideoAlbum)
admin.site.register(Video)