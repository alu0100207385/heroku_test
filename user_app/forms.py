from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

class PictureForm(forms.Form):
    upload = forms.ImageField()