from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    #works even if this isn't present
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'password1', 'password2']

class UserUpdationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']