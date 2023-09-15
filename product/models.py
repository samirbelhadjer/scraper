from django.db import models
from django.conf import settings


class Categorie(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, )
    original_link = models.CharField(max_length=1000, blank=False, null=False, help_text ="this the link where the product is scraped")
    store = models.CharField(max_length=255, blank=False, null=False, help_text ="store where product scraper")
    description = models.TextField(blank=True)
    images =  models.JSONField(null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, blank=True, null=True, related_name='proucts')

    def __str__(self):
        return self.name




