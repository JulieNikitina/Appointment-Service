from django import forms
from django.contrib.auth.forms import UserCreationForm

from appointments.models import User


class SignUp(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
