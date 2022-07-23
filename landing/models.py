from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html
from jalali_date import datetime2jalali
from image_optimizer.fields import OptimizedImageField
from translated_fields import TranslatedField
from django.utils.translation import gettext_lazy as _

class Landing(models.Model):
    title = TranslatedField(models.CharField(max_length=250, verbose_name=_('title')),)
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True, verbose_name=_('link'))
    content = TranslatedField(models.TextField(verbose_name=_('content')),)
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = _('landing')
        verbose_name_plural = _('landings')
        ordering = ['-updated']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        salt = datetime2jalali(self.updated)
        if not self.slug:
            self.slug = slugify(
                self.title_en,
                allow_unicode=True,
            )
        super(Landing, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("landing:detail", kwargs={"slug": self.slug})

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

    admin_thumbnail.short_description = _('image')
    
# Image model
class Image(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name or discription'))
    image = OptimizedImageField(upload_to='landing/images/', verbose_name=_('select file'))
    default = models.BooleanField(default=False, verbose_name=_('default'))
    target = models.ForeignKey(Landing, on_delete=models.CASCADE, related_name='images', verbose_name=_('target'))
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def __str__(self):
        return self.name

    def admin_thumbnail(self):
        return format_html("<img src='{}' width='120px' height='100px' style='border-radius:7px'>".format(self.image.url))

    admin_thumbnail.short_description = _('image')

# Video model
class Video(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name or discription'))
    video = models.FileField(upload_to='landing/videos/', verbose_name=_('select file'))
    default = models.BooleanField(default=False, verbose_name=_('default'))
    target = models.ForeignKey(Landing, on_delete=models.CASCADE, related_name='videos', verbose_name=_('target'))
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __str__(self):
        return self.name

# File model
class File(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name=_('name or discription'))
    item = models.FileField(upload_to='landing/files/', verbose_name=_('select file'))
    default = models.BooleanField(default=False, verbose_name=_('default'))
    target = models.ForeignKey(Landing, on_delete=models.CASCADE, related_name='files', verbose_name=_('target'))
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
        return self.name
