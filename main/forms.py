from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  
from main.models import CustomUser, Comment

class CustomUserCreationForm(UserCreationForm):  
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):  
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = []

class UserSignUp(forms.Form):  
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

class UserLogin(forms.Form):  
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class CommentForm(forms.Form):
    text = forms.CharField(required=True)

class ResponseForm(forms.Form):
    text = forms.CharField(required=True)
    
