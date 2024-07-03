from django.contrib.auth import password_validation
from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Product

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ['full_name','username', 'email', 'password1']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'})}


class LoginForm(AuthenticationForm):
    username= UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Check if the username is actually an email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                username = user.username  # Replace the username with the actual username
            except User.DoesNotExist:
                pass

        self.cleaned_data['username'] = username
        return super().clean()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'Sugar', 'Coffee', 'Flour', 'Chocolate','Milk', 'slug', 'short_description', 'product_image', 'price', 'category']