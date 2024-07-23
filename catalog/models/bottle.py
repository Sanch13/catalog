from django.db import models

from catalog.models.series import Series


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
        FIFE_HUNDRED = '500', '500'
        SEVEN_HUNDRED_FIFTY = '750', '750'
        ONE_THOUSAND = '1000', '1000'

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
    volume = models.CharField(max_length=4,
                              choices=VolumeBottle.choices,
                              default=VolumeBottle.THREE_HUNDRED,
                              verbose_name='Объем мл.')
