from django import forms

from django.contrib.auth.models import User
from localhandsapp.models import Scooper

# scooper owner?
class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(min_length=5, widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")

# Scooper form?
class ScooperForm(forms.ModelForm):
    class Meta:
        model = Scooper
        fields = ("name", "phone", "address", "logo")
