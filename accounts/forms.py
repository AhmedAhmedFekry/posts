from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.forms.widgets import PasswordInput


class SignForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
        # widgets = {
        #     'password': PasswordInput(attrs={'class': 'display_n', }),

        # }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('city', 'country', 'image',)
