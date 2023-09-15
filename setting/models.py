from django.db import models


# Create your models here.
class Setting(models.Model):
    phone_number = models.CharField(blank=False, max_length=13)
    email = models.EmailField(blank=False)
    address = models.CharField(blank=False, max_length=255,)
    google_map_link = models.CharField(blank=False, max_length=1000, help_text="address (google map link)")
    title = models.CharField(max_length=255,blank=False)
    content = models.TextField(blank=False)
    logo = models.ImageField(blank=False)
    colored_logo = models.ImageField(blank=False)
    def __str__(self):
        return "About us settings"

class Contact(models.Model):
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=255,blank=False)
    name = models.CharField(max_length=255,blank=False)
    message = models.TextField(blank=False)
    def __str__(self):
        return "Contact form"