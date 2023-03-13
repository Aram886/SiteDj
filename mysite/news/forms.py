from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import News
import re


class ContactForm(forms.Form):
    subject = forms.CharField(label='Theme', widget=forms.TextInput(attrs={"class": 'form-control'}))
    content = forms.CharField(label='Text', widget=forms.Textarea(attrs={"class": 'form-control', "rows": 5}))
    captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=25, label='User Name',
                               widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=25, label='User Name',
                               help_text="Username could include only 25 symbols",
                               widget=forms.TextInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control", 'rows': 7}),
            'category': forms.Select(attrs={"class": "form-control"})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'[0-9]', title):  # [0-9] or \d
            raise ValidationError('title must not start with number')
        return title
