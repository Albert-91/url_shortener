from django import forms
from django.core.validators import URLValidator
from django.forms import CharField

from url_shortener.models import UrlStore


class UrlStoreForm(forms.ModelForm):
    user_url = CharField(label='URL', validators=[URLValidator()])

    class Meta:
        model = UrlStore
        fields = ['user_url']
