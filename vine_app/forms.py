from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from vine_app import models
from django.forms import ModelForm
from django.forms.widgets import FileInput

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class WineForm(ModelForm):
    class Meta:
        model = models.Wine
        fields = ('shelf_id', 'wine_name', 'winery', 'amount', 'crop_year', 'grape', 'region', 'fragrance', 'taste', 'fun_facts', 'wine_image')

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=FileInput())
