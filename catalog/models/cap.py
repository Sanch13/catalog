from django.db import models
from django.utils.text import slugify

from tinymce.models import HTMLField

from catalog.models.category import Category


class Cap(models.Model):
    class TypeOfClosure(models.TextChoices):
        FLIP_TOP = 'Флип-топ', 'Флип-топ'
        DISK_TOP = 'Диск-топ', 'Диск-топ'
        THREADED_BLIND = 'Резьбовой глухой', 'Резьбовой глухой'
        SPRAY = "Спрей", "Спрей"

    class ThroatStandard(models.TextChoices):
        TWENTY_FOUR = '24/410', '24/410'
        TWENTY_FOUR_ANOTHER = '24/415', '24/415'
        TWENTY_EIGHT = '28/410', '28/410'

    class StatusCap(models.TextChoices):
        REGULAR = 'Обычный', 'Обычный'
        NEW = 'Новинка', 'Новинка'
        BESTSELLER = 'Бестселлер', 'Бестселлер'

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="cap_category",
                                 verbose_name='Категория')
    name = models.CharField(max_length=150,
                            verbose_name='Название')
    slug = models.SlugField(max_length=150,
                            unique=True)
    status = models.CharField(max_length=10,
                              choices=StatusCap.choices,
                              default=StatusCap.REGULAR,
                              verbose_name='Статус товара')
    ratings = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               default=1,
                                               verbose_name='Рейтинг товара')
    type_of_closure = models.CharField(max_length=20,
                                       choices=TypeOfClosure.choices,
                                       default=TypeOfClosure.FLIP_TOP,
                                       verbose_name='Вид укупорки')
    throat_standard = models.CharField(max_length=10,
                                       choices=ThroatStandard.choices,
                                       default=ThroatStandard.TWENTY_FOUR,
                                       verbose_name='Стандарт горла')
    description = HTMLField(blank=True,
                            null=True,
                            verbose_name='Описание')
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Колпачок'
        verbose_name_plural = 'Колпачки'

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
