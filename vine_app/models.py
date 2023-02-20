from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

import hashlib


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
    def get_code_hash(self):
        hash_object = hashlib.sha1(self.user.username.encode('utf-8'))
        return hash_object.hexdigest()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
        return str(self.cabinet) + ":" + self.title
    
    def get_title(self):
        return self.title

class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    shelf_id = models.ForeignKey(Shelf, on_delete=models.SET_NULL, default=0, null=True, blank=True)

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