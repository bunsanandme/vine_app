from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from vine_app import models
from django.forms import ModelForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class WineForm(ModelForm):
    class Meta:
        model = models.Wine
        fields = ('shelf_id', 'winery', 'crop_year', 'region', 'fragrance', 'taste', 'fun_facts', 'wine_image')

class FileUploadForm(forms.Form):
    file = forms.FileField()
