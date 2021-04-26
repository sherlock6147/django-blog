from django.forms import ModelForm
from django import forms
from .models import Comment,ProfilePhoto
from django.contrib.auth.models import User

class UserSignupForm(ModelForm):
    class Meta:
        model= User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150,label='Username')
    password = forms.CharField(max_length=150,label='Password',widget=forms.widgets.PasswordInput)
    
class AddComment(forms.Form):
    comment_text = forms.CharField(max_length=350,label='Add Comment')

class AddProfilePhotoForm(ModelForm):
    class Meta:
        model= ProfilePhoto
        fields= ['profile_image']