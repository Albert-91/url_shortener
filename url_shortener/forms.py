from django import forms
from django.forms import CharField

from url_shortener.models import UrlStore
from url_shortener.validators import validate_url


class UrlStoreForm(forms.ModelForm):
    user_url = CharField(label='URL', validators=[validate_url])

    class Meta:
        model = UrlStore
        fields = ['user_url']
