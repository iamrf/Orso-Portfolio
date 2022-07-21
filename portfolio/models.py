from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html
from jalali_date import datetime2jalali
from image_optimizer.fields import OptimizedImageField

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

    def get_absolute_url(self):
        return reverse("portfolio:detail", kwargs={"slug": self.slug})

    def admin_thumbnail(self):
        try:
            img_url = '#'
            if self.images:
                for img in self.images.all():
                    img_url = img.image.url
                    return format_html("<img src='{}' width='120px' style='border-radius:7px'>".format(img_url))
        except:
            img_url = '#'
        return format_html("<img src='{}' width='120px' style='border-radius:7px'>".format(img_url))

    admin_thumbnail.short_description = 'تصویر'
    
# Image model
class Image(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name='نام و توضیحات')
    image = OptimizedImageField(upload_to='portfolio/images/', verbose_name='انتخاب فایل')
    default = models.BooleanField(default=False, verbose_name='انتخاب به عنوان پیشفرض')
    target = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='images', verbose_name='انتخاب مقصد')
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
    name = models.CharField(max_length=255, blank=True, verbose_name='نام و توضیحات')
    video = models.FileField(upload_to='portfolio/videos/', verbose_name='انتخاب فایل')
    default = models.BooleanField(default=False, verbose_name='انتخاب به عنوان پیشفرض')
    target = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='videos', verbose_name='انتخاب مقصد')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیو ها'

    def __str__(self):
        return self.name

# File model
class File(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name='نام و توضیحات')
    item = models.FileField(upload_to='portfolio/files/', verbose_name='انتخاب فایل')
    default = models.BooleanField(default=False, verbose_name='انتخاب به عنوان پیشفرض')
    target = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='files', verbose_name='انتخاب مقصد')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل ها'

    def __str__(self):
        return self.name
