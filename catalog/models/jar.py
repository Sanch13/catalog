from django.db import models
from django.db.models import Case, When, Value, IntegerField
from django.utils.text import slugify

from tinymce.models import HTMLField

from catalog.models.category import Category


class JarManager(models.Manager):
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


class Jar(models.Model):
    class StatusJar(models.TextChoices):
        REGULAR = 'Обычный', 'Обычный'
        NEW = 'Новинка', 'Новинка'
        BESTSELLER = 'Бестселлер', 'Бестселлер'

    class VolumeJar(models.IntegerChoices):
        FIFTY = 50, '50'
        SEVENTY_FIVE = 75, '75'
        ONE_HUNDRED = 100, '100'
        ONE_HUNDRED_TWENTY = 120, '120'
        ONE_HUNDRED_FIFTY = 150, '150'
        TWO_HUNDRED = 200, '200'
        TWO_HUNDRED_FIFTY = 250, '250'
        THREE_HUNDRED = 300, '300'
        FOUR_HUNDRED = 400, '400'
        FIFE_HUNDRED = 500, '500'

    class SurfaceJar(models.TextChoices):
        GLOSSY = 'глянцевая', 'глянцевая'
        MATTE = 'матовая', 'матовая'

    class YesNoStatusJar(models.TextChoices):
        YES = 'да', 'да'
        NO = 'нет', 'нет'

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="jar_category",
                                 verbose_name='Категория')
    name = models.CharField(max_length=150,
                            verbose_name='Название')
    slug = models.SlugField(max_length=150,
                            unique=True)
    status = models.CharField(max_length=10,
                              choices=StatusJar.choices,
                              default=StatusJar.REGULAR,
                              verbose_name='Статус товара')
    ratings = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               default=1,
                                               verbose_name='Рейтинг товара')
    volume = models.IntegerField(choices=VolumeJar.choices,
                                 default=VolumeJar.TWO_HUNDRED,
                                 verbose_name='Объем мл.')
    surface = models.CharField(max_length=10,
                               choices=SurfaceJar.choices,
                               default=SurfaceJar.GLOSSY,
                               verbose_name="Поверхность")
    double_wall = models.CharField(max_length=3,
                                   choices=YesNoStatusJar.choices,
                                   default=YesNoStatusJar.NO,
                                   verbose_name="Двойная стенка")
    flip_top = models.CharField(max_length=3,
                                choices=YesNoStatusJar.choices,
                                default=YesNoStatusJar.NO,
                                verbose_name="Флип-топ баночка")
    coffe_crumbs = models.CharField(max_length=3,
                                    choices=YesNoStatusJar.choices,
                                    default=YesNoStatusJar.NO,
                                    verbose_name="Экодобавка «кофейная крошка»")
    refil = models.CharField(max_length=3,
                             choices=YesNoStatusJar.choices,
                             default=YesNoStatusJar.NO,
                             verbose_name="Рефил")
    description = HTMLField(blank=True,
                            null=True,
                            verbose_name='Описание')
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата загрузки')

    objects = JarManager()

    class Meta:
        verbose_name = 'Баночка'
        verbose_name_plural = 'Баночки'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(viewname="catalog:product_detail_no_series",
                       args=[self.category.slug, self.slug])
