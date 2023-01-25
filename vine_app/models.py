from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Shelf(models.Model):
    shelf_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"Полка {self.shelf_id}"

class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    shelf_id = models.ForeignKey(Shelf, on_delete=models.CASCADE, default=1)
    wine_name = models.CharField(max_length=50)
    winery = models.CharField(max_length=100, default="")
    crop_year = models.PositiveIntegerField(validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.now().year)],
            help_text="Use the following format: <YYYY>")
    grape = models.CharField(max_length=100, default="")
    region = models.CharField(max_length=60)
    fragrance = models.CharField(max_length=200)
    taste = models.CharField(max_length=200)
    fun_facts = models.TextField()
    wine_image = models.ImageField(upload_to="img/", default="default.jpg")

    def __str__(self):
        return self.wine_name + ", " + str(self.crop_year)
    
    def get_absolute_url(self): # Тут мы создали новый метод
        return reverse('show_wine', args=[str(self.wine_id)])