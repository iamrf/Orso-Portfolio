from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from image_optimizer.fields import OptimizedImageField

def get_image_upload_path(instance, filename):
    try:
        model = instance.album.model.get().__class__._meta
        name = model.verbose_name_plural.replace(' ', '-')
        return f'{name}/images/{filename}'
    except:
        return f'images/{filename}'

def get_video_upload_path(instance, filename):
    try:
        model = instance.album.model.get().__class__._meta
        name = model.verbose_name_plural.replace(' ', '-')
        return f'{name}/videos/{filename}'
    except:
        return f'videos/{filename}'

def get_file_upload_path(instance, filename):
    try:
        model = instance.album.model.get().__class__._meta
        name = model.verbose_name_plural.replace(' ', '-')
        return f'{name}/files/{filename}'
    except:
        return f'files/{filename}'

# Image Album model
class ImageAlbum(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام آلبوم')

    class Meta:
        verbose_name = 'آلبوم تصاویر'
        verbose_name_plural = 'آلبوم تصاویر'

    def __str__(self):
        return self.name

    def default(self):
        return self.images.filter(default=True).first()

# Video Album model
class VideoAlbum(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام آلبوم')

    class Meta:
        verbose_name = 'آلبوم ویدیو'
        verbose_name_plural = 'آلبوم ویدیوها'

    def __str__(self):
        return self.name

    def default(self):
        return self.videos.filter(default=True).first()

# File Album model
class FileAlbum(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام آلبوم')

    class Meta:
        verbose_name = 'آلبوم فایل'
        verbose_name_plural = 'آلبوم فایل ها'

    def __str__(self):
        return self.name

    def default(self):
        return self.files.filter(default=True).first()

# Image model
class Image(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام و توضیحات')
    image = OptimizedImageField(upload_to=get_image_upload_path, verbose_name='انتخاب فایل')
    default = models.BooleanField(default=False, verbose_name='انتخاب به عنوان پیشفرض')
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, related_name='images', verbose_name='انتخاب آلبوم')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def __str__(self):
        return self.name
    
    def admin_thumbnail(self):
        return format_html("<img src='{}' width='120px' height='100px' style='border-radius:7px'>".format(self.image.url))

    admin_thumbnail.short_description = 'تصویر'

# Video model
class Video(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام و توضیحات')
    video = models.FileField(upload_to=get_video_upload_path, verbose_name='انتخاب فایل')
    default = models.BooleanField(default=False, verbose_name='انتخاب به عنوان پیشفرض')
    album = models.ForeignKey(VideoAlbum, on_delete=models.CASCADE, related_name='videos', verbose_name='انتخاب آلبوم')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیو ها'

    def __str__(self):
        return self.name

# File model
class File(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام و توضیحات')
    item = models.FileField(upload_to=get_file_upload_path, verbose_name='انتخاب فایل')
    default = models.BooleanField(default=False, verbose_name='انتخاب به عنوان پیشفرض')
    album = models.ForeignKey(FileAlbum, on_delete=models.CASCADE, related_name='files', verbose_name='انتخاب لیست')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل ها'

    def __str__(self):
        return self.name
