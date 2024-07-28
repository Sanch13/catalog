from django.db import models
from django.utils.text import slugify

from tinymce.models import HTMLField

from catalog.models.series import Series
from catalog.models.category import Category


class Bottle(models.Model):
    class StatusBottle(models.TextChoices):
        REGULAR = 'Обычный', 'Обычный'
        NEW = 'Новинка', 'Новинка'
        BESTSELLER = 'Бестселлер', 'Бестселлер'

    class VolumeBottle(models.TextChoices):
        THIRTY = '30', '30'
        FIFTY = '50', '50'
        SIXTY_FIVE = '65', '65'
        EIGHTY = '80', '80'
        NINETY = '90', '90'
        ONE_HUNDRED = '100', '100'
        ONE_HUNDRED_TWENTY_FIVE = '125', '125'
        ONE_HUNDRED_FIFTY = '150', '150'
        TWO_HUNDRED = '200', '200'
        TWO_HUNDRED_TEN = '210', '210'
        TWO_HUNDRED_FIFTY = '250', '250'
        THREE_HUNDRED = '300', '300'
        THREE_HUNDRED_TEN = '310', '310'
        THREE_HUNDRED_FIFTY = '350', '350'
        THREE_HUNDRED_SEVENTY = '370', '370'
        FOUR_HUNDRED = '400', '400'
        FOUR_HUNDRED_FIFTY = '450', '450'
        FIFE_HUNDRED = '500', '500'
        SEVEN_HUNDRED_FIFTY = '750', '750'
        ONE_THOUSAND = '1000', '1000'

    class ShapeBottle(models.TextChoices):
        CYLINDER = 'цилиндричекая', 'цилиндричекая'
        SQUARE = 'квадратная', 'квадратная'
        CIRCLE = 'круглая', 'круглая'

    class ThroatStandard(models.TextChoices):
        TWENTY_FOUR = '24/410', '24/410'
        TWENTY_FOUR_ANOTHER = '24/415', '24/415'
        TWENTY_EIGHT = '28/410', '28/410'

    class SurfaceBottle(models.TextChoices):
        SOFT_TOUCH = 'софт тач', 'софт тач'
        NO_SOFT_TOUCH = 'без софт тач', 'без софт тач'

    class YesNoStatusBottle(models.TextChoices):
        YES = 'да', 'да'
        NO = 'нет', 'нет'

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="bottle_category",
                                 verbose_name='Категория товара')
    series = models.ForeignKey(Series,
                               on_delete=models.CASCADE,
                               related_name="bottle",
                               verbose_name='Серия')
    name = models.CharField(max_length=150,
                            verbose_name='Название')
    slug = models.SlugField(max_length=150,
                            unique=True)
    status = models.CharField(max_length=10,
                              choices=StatusBottle.choices,
                              default=StatusBottle.REGULAR,
                              verbose_name='Статус товара')
    ratings = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               default=1,
                                               verbose_name='Рейтинг товара')
    volume = models.CharField(max_length=5,
                              choices=VolumeBottle.choices,
                              default=VolumeBottle.THREE_HUNDRED,
                              verbose_name='Объем мл.')
    shape = models.CharField(max_length=15,
                             choices=ShapeBottle.choices,
                             default=ShapeBottle.CYLINDER,
                             verbose_name='Форма')
    throat_standard = models.CharField(max_length=10,
                                       choices=ThroatStandard.choices,
                                       default=ThroatStandard.TWENTY_FOUR,
                                       verbose_name='Стандарт горла')
    surface = models.CharField(max_length=15,
                               choices=SurfaceBottle.choices,
                               default=SurfaceBottle.SOFT_TOUCH,
                               verbose_name="Поверхность")
    coffe_crumbs = models.CharField(max_length=3,
                                    choices=YesNoStatusBottle.choices,
                                    default=YesNoStatusBottle.NO,
                                    verbose_name="Экодобавка «кофейная крошка»")
    full_color_or_silkscreen = models.CharField(max_length=3,
                                                choices=YesNoStatusBottle.choices,
                                                default=YesNoStatusBottle.NO,
                                                verbose_name="Доступен полноцвет или шелкография")
    description = HTMLField(blank=True,
                            null=True,
                            verbose_name='Описание')
    decoration = HTMLField(blank=True,
                           null=True,
                           verbose_name="Декорирование")
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Флакон'
        verbose_name_plural = 'Флаконы'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(viewname="catalog:product_detail",
                       args=[self.category.slug, self.series.slug, self.slug])
