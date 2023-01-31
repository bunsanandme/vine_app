from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Shelf(models.Model):
    shelf_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.title

class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    shelf_id = models.ForeignKey(Shelf, on_delete=models.CASCADE, default=0)
    wine_name = models.CharField(max_length=50, default="")
    winery = models.CharField(max_length=100, default="")

    crop_year = models.PositiveIntegerField(default=1900, validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.now().year)],
            help_text="Use the following format: <YYYY>")
    grape = models.CharField(max_length=100, default="")
    region = models.CharField(max_length=60, default="")
    
    fragrance = models.TextField(max_length=200, default="")
    taste = models.TextField(max_length=200, default="")
    fun_facts = models.TextField(default="")
    wine_image = models.ImageField(upload_to="img/", default="default.jpg")

    def __str__(self):
        return self.wine_name + ", " + str(self.crop_year)
    
    def get_absolute_url(self): # Тут мы создали новый метод
        return reverse('show_wine', args=[str(self.wine_id)])