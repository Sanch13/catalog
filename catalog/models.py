import os

from django.db import models


def get_upload_path_category_images(instance, filename):
    return os.path.join('files', instance.name, filename)


class Category(models.Model):
    class Categories(models.TextChoices):
        BOTTLES = 'флаконы', 'флаконы'
        JARS = 'баночки', 'баночки'
        CAPS = 'колпачки', 'колпачки'
        NEWS = 'новинки', 'новинки'

    name = models.CharField(max_length=50,
                            unique=True,
                            choices=Categories.choices,
                            default=Categories.BOTTLES)
    slug = models.SlugField(max_length=50,
                            unique=True)
    description = models.TextField(blank=True,
                                   null=True)
    category_image = models.ImageField(upload_to=get_upload_path_category_images,
                                       blank=True,
                                       null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    is_new = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Flask(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    volume = models.CharField(max_length=100)  # Example attribute

    def __str__(self):
        return f"{self.product.name} ({self.volume})"


class Jar(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    material = models.CharField(max_length=100)  # Example attribute

    def __str__(self):
        return f"{self.product.name} ({self.material})"


class Cap(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    diameter = models.DecimalField(max_digits=5, decimal_places=2)  # Example attribute

    def __str__(self):
        return f"{self.product.name} ({self.diameter} mm)"


# class Cap(models.Model):
#     class ProductStatus(models.TextChoices):
#         REGULAR = 'Обычный', 'Обычный'
#         NEW = 'Новинка', 'Новинка'
#         BESTSELLER = 'Бестселлер', 'Бестселлер'
#
#     class TypeOfClosure(models.TextChoices):
#         FLIP_TOP = 'Флип-топ', 'Флип-топ'
#         DISK_TOP = 'Диск-топ', 'Диск-топ'
#         THREADED_BLIND = 'Резьбовой глухой', 'Резьбовой глухой'
#
#     class Surface(models.TextChoices):
#         COMBINATION = ('Комбинированная (сочетание глянцевой и матовой)',
#                        'Комбинированная (сочетание глянцевой и матовой)')
#         GLOSSY = 'Глянцевая', 'Глянцевая'
#         MATTE = 'Матовая', 'Матовая'
#
#     class ThroatStandard(models.TextChoices):
#         TWENTY_FOUR = '24/410', '24/410'
#         TWENTY_EIGHT = '28/410', '28/410'
#
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=100,
#                             unique=True)
#     status = models.CharField(max_length=20,
#                               choices=ProductStatus.choices,
#                               default=ProductStatus.REGULAR)
#     category = models.ForeignKey(Category,
#                                  on_delete=models.CASCADE,
#                                  related_name='products')
#     description = models.TextField(blank=True,
#                                    null=True)
#     type_of_closure = models.CharField(max_length=20,
#                                        choices=TypeOfClosure.choices,
#                                        default=TypeOfClosure.FLIP_TOP)
#     surface = models.CharField(max_length=50,
#                                choices=Surface.choices,
#                                default=Surface.GLOSSY)
#     throat_standard = models.CharField(max_length=10,
#                                        choices=ThroatStandard.choices,
#                                        default=ThroatStandard.TWENTY_FOUR)
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)
#
#
# def get_file_upload_path_caps(instance, filename):
#     return os.path.join('files', instance.cap.category.name, instance.cap.name, filename)
#
#
# class FileCap(models.Model):
#     cap = models.ForeignKey(Cap,
#                             on_delete=models.CASCADE,
#                             related_name='files_cap')
#     file = models.FileField(upload_to=get_file_upload_path_caps,
#                             blank=True,
#                             null=True)
#
#     objects = models.Manager()
