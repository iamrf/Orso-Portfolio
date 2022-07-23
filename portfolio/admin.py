from django.contrib import admin
from django import forms
from .models import Category, Portfolio, Image, Video, File
from jalali_date import datetime2jalali
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import gettext_lazy as _

# Create a form for PostAdmin fields widgets
class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        widgets = {
            'description_fa' : CKEditorUploadingWidget(),
            'description_en' : CKEditorUploadingWidget(),
        }
        fields = '__all__'

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    classes = ('collapse',)
    
class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    classes = ('collapse',)
    
class FileInline(admin.TabularInline):
    model = File
    extra = 1
    classes = ('collapse',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    form = PortfolioForm
    inlines = [ImageInline, VideoInline, FileInline]
    filter_horizontal = ['category']
    fieldsets = (
        (_('title'),{
            'fields' : ('title_fa', 'title_en', 'slug')
        }),
        (_('content'),{
            'fields' : ('description_fa', 'description_en',)
        }),
        (_('category'),{
            'fields' : ('category',)
        }),
        (_('active / deactive'),{
            'fields' : ('is_active',)
        }),
    )
    list_display = ['title', 'admin_thumbnail', 'is_active', 'get_created', 'get_updated']
    ordering = ['-updated']

    def get_created(self, obj):
        return datetime2jalali(obj.created).strftime('%A %-d %B %Y ساعت %H:%M')
    def get_updated(self, obj):
        return datetime2jalali(obj.updated).strftime('%A %-d %B %Y ساعت %H:%M')
 
    get_created.short_description = _('created')
    get_created.admin_order_field = 'created'
    get_updated.short_description = _('updated')
    get_updated.admin_order_field = 'updated'


admin.site.register(Category)