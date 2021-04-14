from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class UserSignupForm(ModelForm):
    class Meta:
        model= User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150,label='Username')
    password = forms.CharField(max_length=150,label='Password',widget=forms.widgets.PasswordInput)
    