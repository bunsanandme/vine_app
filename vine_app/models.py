from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Cabinet(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=50, default="Шкаф")
    description = models.TextField(default="Описание винного шкафа дополнительно")

    def __str__(self):
        return self.title
    
class Shelf(models.Model):
    cabinet = models.ForeignKey(Cabinet, on_delete=models.SET_NULL, default=1, null=True, blank=True)
    title = models.CharField(max_length=50, default="Полка")
    description = models.TextField(default="Представляем коллекцию вин, отобранную со вкусом и знанием своего дела")

    def __str__(self):
        return self.title

class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    shelf_id = models.ForeignKey(Shelf, on_delete=models.CASCADE, default=0)

    amount = models.IntegerField(default=0)
    wine_name = models.CharField(max_length=50, default="")
    winery = models.CharField(max_length=100, default="")

    crop_year = models.PositiveIntegerField(default=1900, validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.now().year)])
    grape = models.CharField(max_length=100, default="")
    region = models.CharField(max_length=60, default="")
    
    fragrance = models.TextField(max_length=200, default="")
    taste = models.TextField(max_length=200, default="")
    fun_facts = models.TextField(default="")
    wine_image = models.ImageField(upload_to="img/", default="default.jpg")

    def __str__(self):
        return self.wine_name + ", " + str(self.crop_year)
    
    def get_absolute_url(self):
        return reverse('show_wine', args=[str(self.wine_id)])