from django.db import models
from django.utils import timezone

class Item(models.Model):
    category1 = models.CharField(max_length=20)
    category2 = models.CharField(max_length=20)
    img = models.CharField(max_length=100)

class Design(models.Model):
    item_id = models.IntegerField(default=0)
    category1 = models.CharField(max_length=20)
    category2 = models.CharField(max_length=20)
    date = models.DateField(default = timezone.now)
    title = models.CharField(max_length=20)
    img = models.CharField(max_length=100)