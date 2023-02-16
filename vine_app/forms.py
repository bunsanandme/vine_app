from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from vine_app import models
from django.forms import ModelForm
from django.forms.widgets import FileInput
from django.core.exceptions import ValidationError 


class UserRegisterForm(UserCreationForm): 
    username = forms.CharField(label='username', min_length=5, max_length=150) 
    email = forms.EmailField(label='email') 
    password1 = forms.CharField(label='password', widget=forms.PasswordInput) 
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput) 
 
    def username_clean(self): 
        username = self.cleaned_data['username'].lower() 
        new = User.objects.filter(username = username) 
        if new.count(): 
            raise ValidationError("User Already Exist") 
        return username 
 
    def email_clean(self): 
        email = self.cleaned_data['email'].lower() 
        new = User.objects.filter(email=email) 
        if new.count(): 
            raise ValidationError(" Email Already Exist") 
        return email 
 
    def clean_password2(self): 
        password1 = self.cleaned_data['password1'] 
        password2 = self.cleaned_data['password2'] 
 
        if password1 and password2 and password1 != password2: 
            raise ValidationError("Password don't match") 
        return password2 
 
    def save(self, commit = True): 
        user = User.objects.create_user( 
            self.cleaned_data['username'], 
            self.cleaned_data['email'], 
            self.cleaned_data['password1'] 
        ) 
        return user

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class WineForm(ModelForm):
    class Meta:
        model = models.Wine
        fields = ('shelf_id', 'wine_name', 'winery', 'amount', 'crop_year', 'grape', 'region', 'fragrance', 'taste', 'fun_facts', 'wine_image')

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=FileInput())

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ("phone_number", "address")