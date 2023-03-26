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



class BookingForm(forms.Form):
    ROOM_TYPES = [
        ('ac', 'AC'),
        ('nonac', 'NonAC'),
    ]
    BEDS = [
        ('0', 'Select an option'),
        ('1', 'Single Bed'),
        ('2', 'Double Bed'),
        ('3', 'Triple Bed'),
    ]

    room_type = forms.ChoiceField(
        choices=ROOM_TYPES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control-sm', 'style': 'width:150px;'})
    )

    bed_type = forms.ChoiceField(
        choices=BEDS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control-sm', 'style': 'width:150px;'})
    )

    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control-sm'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control-sm'}))

    # The clean method is used to validate the form data and ensure that the selected dates are valid and the room is available for booking. It checks for overlapping bookings using the filter method on the bookings queryset, and raises a ValidationError if any conflicts are found. It also checks that the check-in date is not in the past, and that the check-out date is after the check-in date.
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            if check_in_date < timezone.now().date():
                raise forms.ValidationError("The check-in date cannot be in the past.")
            if check_out_date < check_in_date:
                raise forms.ValidationError("The check-out date must be after the check-in date.")

        return cleaned_data

    def get_non_field_errors(self):
        errors = super().get_non_field_errors()
        errors.extend(self.non_field_errors())
        return errors