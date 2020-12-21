from django.db import models

# Create your models here.

class SiteList(models.Model):
    ip_addr = models.CharField(verbose_name='IP Address',max_length=20)
    valid = models.BooleanField(verbose_name='Allowed')