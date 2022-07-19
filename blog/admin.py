from django.contrib import admin
from django import forms
from .models import Tag, Post
from jalali_date import datetime2jalali
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Create a form for PostAdmin fields widgets
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'content' : CKEditorUploadingWidget(),
        }
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    filter_horizontal = ['tags']
    fieldsets = (
        ('عنوان',{
            'fields' : ('title', 'slug')
        }),
        ('محتوا',{
            'fields' : ('content',)
        }),
        ('تگ ها',{
            'fields' : ('tags',)
        }),
        ('فعال/ غیرفعال',{
            'fields' : ('is_active',)
        }),
    )
    list_display = ['title', 'is_active', 'get_created', 'get_updated']
    ordering = ['-updated']

    def get_created(self, obj):
        return datetime2jalali(obj.created).strftime('%A %-d %B %Y ساعت %H:%M')
    def get_updated(self, obj):
        return datetime2jalali(obj.updated).strftime('%A %-d %B %Y ساعت %H:%M')
 
    get_created.short_description = 'تاریخ ایجاد'
    get_created.admin_order_field = 'created'
    get_updated.short_description = 'آخرین ویرایش'
    get_updated.admin_order_field = 'updated'


admin.site.register(Tag)
