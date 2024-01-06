from django.db import models
from django.utils import timezone

class Item(models.Model):
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    path = models.CharField(max_length=100)
    size = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

class Design(models.Model):
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    date = models.DateField(default = timezone.now)
    path = models.CharField(max_length=100)