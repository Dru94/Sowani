from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }

        labels = {}


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')