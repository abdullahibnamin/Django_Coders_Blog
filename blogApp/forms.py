from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User

# from tinymce import models as tinymce_models
# from tinymce.widgets import TinyMCE


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': "Email"
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# class UserBlogForm(ModelForm):
#     id_desc = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
#     class Meta:
#         model = Blog_post
#         fields = ['title', 'desc']

#         labels = {
#             'title': 'Title',
#             'desc': 'Description'
#         }
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'desc': forms.TextInput(attrs={'class': 'form-control'})
#         }

