import os

from django.db import models
from django.db.models import Case, When, Value, IntegerField
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from catalog.models.category import Category
from catalog.utils import convert_img_to_webp


def get_upload_path_series(instance, filename):
    category = instance.category.name
    series_name = instance.name
    return os.path.join('files', category, series_name, filename)


class SeriesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            status_order=Case(
                When(status='Новинка', then=Value(1)),
                When(status='Бестселлер', then=Value(2)),
                When(status='Обычный', then=Value(3)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-ratings')


class Series(models.Model):
    class StatusSeries(models.TextChoices):
        REGULAR = 'Обычный', 'Обычный'
        NEW = 'Новинка', 'Новинка'
        BESTSELLER = 'Бестселлер', 'Бестселлер'
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="series",
                                 verbose_name="Категория товара")
    name = models.CharField(max_length=50,
                            verbose_name='Серия')
    slug = models.SlugField(max_length=50,
                            unique=True)
    status = models.CharField(max_length=10,
                              choices=StatusSeries.choices,
                              default=StatusSeries.REGULAR,
                              verbose_name='Статус товара')
    ratings = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               default=1,
                                               verbose_name='Рейтинг серии')
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание')
    series_image = models.ImageField(upload_to=get_upload_path_series,
                                     blank=True,
                                     null=True,
                                     verbose_name="Изображение серии")
    thumbnail = ImageSpecField(source='series_image',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})

    objects = SeriesManager()

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
        ordering = ["-ratings"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        image_content = convert_img_to_webp(image=self.series_image)
        self.series_image.save(image_content.name, image_content, save=False)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        first_bottle = self.bottle.order_by('volume').first()
        if first_bottle:
            return reverse(viewname="catalog:product_detail",
                           args=[self.category.slug, self.slug, first_bottle.slug])
