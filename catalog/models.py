from django.db import models
from django.utils.text import slugify

from .utils import get_file_upload_path_category, get_upload_path_category_images


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
                            help_text="Наименование")
    slug = models.SlugField(max_length=50,
                            unique=True)
    description = models.TextField(blank=True,
                                   null=True)
    category_image = models.ImageField(upload_to=get_upload_path_category_images,
                                       blank=True,
                                       null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    class ProductStatus(models.TextChoices):
        REGULAR = 'Обычный', 'Обычный'
        NEW = 'Новинка', 'Новинка'
        BESTSELLER = 'Бестселлер', 'Бестселлер'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,
                            unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=ProductStatus.choices,
                              default=ProductStatus.REGULAR)
    description = models.TextField(blank=True,
                                   null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Series(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,
                            unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True,
                                   null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Flask(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    volume = models.SmallIntegerField()  # Example attribute

    def __str__(self):
        return f"{self.product.name} ({self.volume})"


class Jar(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    material = models.CharField(max_length=100)  # Example attribute

    def __str__(self):
        return f"{self.product.name} ({self.material})"


class Cap(models.Model):
    class Surface(models.TextChoices):
        COMBINATION = ('Комбинированная (сочетание глянцевой и матовой)',
                       'Комбинированная (сочетание глянцевой и матовой)')
        GLOSSY = 'Глянцевая', 'Глянцевая'
        MATTE = 'Матовая', 'Матовая'

    class TypeOfClosure(models.TextChoices):
        FLIP_TOP = 'Флип-топ', 'Флип-топ'
        DISK_TOP = 'Диск-топ', 'Диск-топ'
        THREADED_BLIND = 'Резьбовой глухой', 'Резьбовой глухой'

    class ThroatStandard(models.TextChoices):
        TWENTY_FOUR = '24/410', '24/410'
        TWENTY_EIGHT = '28/410', '28/410'

    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    type_of_closure = models.CharField(max_length=20,
                                       choices=TypeOfClosure.choices,
                                       default=TypeOfClosure.FLIP_TOP)
    surface = models.CharField(max_length=50,
                               choices=Surface.choices,
                               default=Surface.GLOSSY)
    throat_standard = models.CharField(max_length=10,
                                       choices=ThroatStandard.choices,
                                       default=ThroatStandard.TWENTY_FOUR)

    def __str__(self):
        return f"{self.product.name}"


class File(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="files")
    file = models.FileField(upload_to=get_file_upload_path_category)
