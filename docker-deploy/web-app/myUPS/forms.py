from django import forms
from django.contrib.auth.models import User

from .models import Package
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class  RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class EditDesForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = ['dest_x', 'dest_y']

class EmailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']


# class RegisterForm(UserCreationForm):
#     class Meta:
#         fields = ("username", "email", "password1", "password2")
#         model = get_user_model()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].label = "Display name"
#         self.fields["email"].label = "Email address"