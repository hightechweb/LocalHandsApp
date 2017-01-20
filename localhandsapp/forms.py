from django import forms

from django.contrib.auth.models import User
from localhandsapp.models import Scooper

# UserForm
class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")

# UserForm for edit account
class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

# ScooperForm for signup
class ScooperForm(forms.ModelForm):
    class Meta:
        model = Scooper
        fields = ("name", "phone", "address", "logo")
