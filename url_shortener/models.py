import base64
from typing import Text

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from url_shortener.mixins import Timestamps


class Url(Timestamps, models.Model):

    regex = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    user_url = models.URLField(_("User URL"), blank=False, max_length=1000, null=False, unique=True,
                               validators=[RegexValidator(regex=regex, message='Invalid URL')])
    url_hash = models.URLField(_("Hash URL"), blank=False, max_length=200, null=False, unique=True)

    class Meta:
        db_table = "url"
        verbose_name = _("url")
        verbose_name_plural = _("urls")

    def save(self, *args, **kwargs):
        self.url_hash = self.encode_url(self.user_url)
        super().save(*args, **kwargs)

    @staticmethod
    def encode_url(url: Text) -> Text:
        return base64.b64encode(bytes(url, encoding='utf-8')).decode(encoding='utf-8')[:200]
