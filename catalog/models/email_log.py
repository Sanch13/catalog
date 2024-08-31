from django.db import models


class EmailLog(models.Model):

    class LeadQualification(models.TextChoices):
        CUSTOMER = 'покупатель', 'покупатель'
        SUPPLIER = 'поставщик', 'поставщик'

    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    comment = models.TextField()
    category = models.CharField(max_length=255)
    place = models.CharField(max_length=55)
    status = models.CharField(max_length=255)
    products = models.TextField()
    lead_qualification = models.CharField(max_length=10,
                                          choices=LeadQualification.choices,
                                          default=LeadQualification.CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} from {self.place} category {self.category}"
