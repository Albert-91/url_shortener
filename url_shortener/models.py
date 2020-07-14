import os
from hashlib import blake2b
from typing import Text
from urllib.parse import urlunparse

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from url_shortener.mixins import Timestamps


class Url(Timestamps, models.Model):

    regex = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    user_url = models.URLField(_("URL"), blank=False, max_length=1000, null=False, unique=True,
                               validators=[RegexValidator(regex=regex, message='Invalid URL')])
    url_hash = models.URLField(_("Hash URL"), blank=False, max_length=200, null=False, unique=True)

    class Meta:
        db_table = "url"
        verbose_name = _("url")
        verbose_name_plural = _("urls")

    def get_short_url(self, request) -> Text:
        scheme, host = request.META['wsgi.url_scheme'], request.META['HTTP_HOST']
        return urlunparse((scheme, host, self.url_hash, None, None, None))

    def save(self, *args, **kwargs):
        self.url_hash = self.encode_url(self.user_url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.user_url

    @staticmethod
    def encode_url(url: Text) -> Text:
        salt = os.urandom(blake2b.SALT_SIZE)
        return blake2b(bytes(url, encoding='utf-8'), digest_size=10, salt=salt).hexdigest()
