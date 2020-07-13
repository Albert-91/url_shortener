from django import forms

from url_shortener.models import Url


class UrlForm(forms.ModelForm):

    class Meta:
        model = Url
        fields = ['user_url']
