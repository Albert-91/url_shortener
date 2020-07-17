from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from url_shortener.mixins import Timestamps
from .utils import encode_string


class UrlStore(Timestamps, models.Model):

    user_url = models.URLField(_("URL"), blank=False, max_length=1000, null=False, validators=[URLValidator()])
    url_hash = models.CharField(_("Hash URL"), blank=False, max_length=200, null=False, unique=True)

    class Meta:
        db_table = "url store"
        verbose_name = _("url store")
        verbose_name_plural = _("urls store")

    def __str__(self):
        return self.user_url

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = encode_string(s=self.user_url, size=getattr(settings, "SHORT_URL_DEFAULT_LENGTH", 10))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.user_url

    def get_short_url(self):
        return 'http://{}/{}'.format(getattr(settings, "DOMAIN_NAME"), self.url_hash)
