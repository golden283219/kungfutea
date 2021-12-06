import uuid
from django.db import models

class MenuLink(models.Model):
    Label = models.CharField(max_length=1024)
    Link = models.CharField(max_length=1024)
    BackButton = models.BooleanField(default=False, verbose_name="BackButton Support")
    def __str__(self):
        return self.Label

class QuickLink(models.Model):
    Label = models.CharField(max_length=1024)
    Link = models.CharField(max_length=1024)
    Icon = models.FileField(null=True)
    BackButton = models.BooleanField(default=False, verbose_name="BackButton Support")
    def __str__(self):
        return self.Label
