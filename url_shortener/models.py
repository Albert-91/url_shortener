import os
from hashlib import blake2b
from typing import Text
from urllib.parse import urlunparse

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from url_shortener.mixins import Timestamps
from .validators import validate_url


class UrlStore(Timestamps, models.Model):

    user_url = models.URLField(_("URL"), blank=False, max_length=1000, null=False, unique=True, validators=[validate_url])
    url_hash = models.CharField(_("Hash URL"), blank=False, max_length=200, null=False, unique=True)

    class Meta:
        db_table = "url store"
        verbose_name = _("url store")
        verbose_name_plural = _("urls store")

    def __str__(self):
        return self.user_url

    def get_short_url(self, request) -> Text:
        scheme, host = request.META['wsgi.url_scheme'], request.META['HTTP_HOST']
        return urlunparse((scheme, host, self.url_hash, None, None, None))

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = self.encode_url(self.user_url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.user_url

    @staticmethod
    def encode_url(url: Text) -> Text:
        salt = os.urandom(blake2b.SALT_SIZE)
        return blake2b(bytes(url, encoding='utf-8'), digest_size=getattr(settings, "SHORT_URL_DEFAULT_LENGTH", 10), salt=salt).hexdigest()
