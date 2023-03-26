from django.utils import timezone
from django import forms
from .models import *
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    uname = forms.CharField(
        label="Username", min_length=3, max_length=20, required=True,
        validators=[RegexValidator(r"^[a-zA-ZÀ-ÿ\s]*$", message="Only Letters allowed !")],
        widget=forms.TextInput(attrs={'class': 'form-control-sm', 'name': 'username', 'id': 'username'})
    )

    email_address = forms.EmailField(
        label="Email Address", min_length=8, max_length=50, required=True,
        validators=[RegexValidator(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$", message="Put a valid email address !")],
        widget=forms.EmailInput(attrs={'class': 'form-control-sm'})
    )

    password = forms.CharField(
        label="Password", min_length=3, max_length=50, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control-sm'})
    )

    phoneNumber = forms.CharField(
        label="Phone Number", min_length=10, max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control-sm'})
    )


class LoginForm(forms.Form):
    uname = forms.CharField(
        label="Username", min_length=3, max_length=20, required=True,
        validators=[RegexValidator(r"^[a-zA-ZÀ-ÿ\s]*$", message="Only Letters allowed !")],
        widget=forms.TextInput(attrs={'class': 'form-control-sm', 'name': 'username', 'id': 'username'})
    )

    password = forms.CharField(
        label="Password", min_length=3, max_length=50, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control-sm'})
    )