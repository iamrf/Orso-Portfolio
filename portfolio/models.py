from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from jalali_date import datetime2jalali
from image_optimizer.fields import OptimizedImageField
from media.models import ImageAlbum, VideoAlbum

class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='عنوان')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True, verbose_name='لینک')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'موضوع'
        verbose_name_plural = 'موضوع ها'
        ordering = ['-updated']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.name,
                allow_unicode=True,
            )
        super(Category, self).save(*args, **kwargs)


class Portfolio(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True, verbose_name='لینک')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    category = models.ManyToManyField(Category, blank=True, verbose_name='موضوع ها')
    image = OptimizedImageField(upload_to='images/', blank=True, verbose_name='انتخاب عکس')
    video = models.FileField(upload_to='videos/', blank=True, verbose_name='انتخاب ویدیو')
    images = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, blank=True, null=True, related_name='model', verbose_name='آلبوم تصاویر')
    videos = models.ForeignKey(VideoAlbum, on_delete=models.CASCADE, blank=True, null=True, related_name='model', verbose_name='آلبوم ویدیو ها')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'پورتفوی'
        verbose_name_plural = 'پورتفوی ها'
        ordering = ['-updated']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        salt = datetime2jalali(self.updated)
        if not self.slug:
            self.slug = slugify(
                self.title,
                allow_unicode=True,
            )
        super(Portfolio, self).save(*args, **kwargs)

    def admin_thumbnail(self):
        try:
            img_url = '#'
            if self.images:
                for img in self.images.images.all():
                    img_url = img.image.url
                    return format_html("<img src='{}' width='120px' style='border-radius:7px'>".format(img_url))
        except:
            img_url = '#'
        return format_html("<img src='{}' width='120px' style='border-radius:7px'>".format(img_url))

    admin_thumbnail.short_description = 'تصویر'