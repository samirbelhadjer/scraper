from django.db import models
from django.conf import settings


# Create your models here.
class Ad(models.Model):
    STATUS_CHOICES = (
        ('Top', 'top'),
        ('Side', 'side'),
    )
    is_active = models.BooleanField(blank=False)
    photo = models.ImageField(upload_to="banner/", null=False, blank=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    position = models.CharField(max_length=4, choices=STATUS_CHOICES, null=False, blank=False)
    
    def __str__(self):
        return self.title