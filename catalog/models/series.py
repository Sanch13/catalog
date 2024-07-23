from django.db import models
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from catalog.models.category import Category
from catalog.utils import get_default_category, get_upload_path_category_or_series


class Series(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="series",
                                 verbose_name="Категория товара",
                                 default=get_default_category)
    name = models.CharField(max_length=50,
                            verbose_name='Серия')
    slug = models.SlugField(max_length=50,
                            unique=True)
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание')
    series_image = models.ImageField(upload_to=get_upload_path_category_or_series,
                                     blank=True,
                                     null=True,
                                     verbose_name="Изображение серии")
    thumbnail = ImageSpecField(source='series_image',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        pass
