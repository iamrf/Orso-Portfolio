from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from jalali_date import datetime2jalali

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True, verbose_name='لینک')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'
        ordering = ['-updated']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.name,
                allow_unicode=True,
            )
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان')
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True, verbose_name='لینک')
    content = models.TextField(verbose_name='محتوا')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='تگ ها')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
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
        super(Post, self).save(*args, **kwargs)

