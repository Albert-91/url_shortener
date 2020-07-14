from django import forms

from url_shortener.models import UrlStore


class UrlStoreForm(forms.ModelForm):

    class Meta:
        model = UrlStore
        fields = ['user_url']
