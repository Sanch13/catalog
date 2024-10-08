from django.db import models
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from catalog.utils import convert_img_to_webp, get_upload_path_category


class Category(models.Model):
    class Categories(models.TextChoices):
        BOTTLES = 'Флаконы', 'Флаконы'
        JARS = 'Баночки', 'Баночки'
        CAPS = 'Колпачки', 'Колпачки'
        NEWS = 'Новинки', 'Новинки'

    name = models.CharField(max_length=50,
                            unique=True,
                            choices=Categories.choices,
                            default=Categories.BOTTLES,
                            verbose_name='Название')
    slug = models.SlugField(max_length=50,
                            unique=True)
    rating = models.PositiveSmallIntegerField(blank=True,
                                              null=True,
                                              default=1,
                                              verbose_name='Порядок фотографий')
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание')
    category_image = models.ImageField(upload_to=get_upload_path_category,
                                       blank=True,
                                       null=True,
                                       verbose_name='Изображение категории')
    thumbnail = ImageSpecField(source='category_image',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = [
            "-rating",
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if not self.pk:
            image_content = convert_img_to_webp(image=self.category_image)
            self.category_image.save(image_content.name, image_content, save=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(viewname="catalog:category", args=[self.slug])
