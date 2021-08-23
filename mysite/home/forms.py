from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

class registration_form(UserCreationForm):
    Email = forms.EmailField(max_length=50)
    class Meta:
        model = User
        fields = ["username","Email","password1","password2"]