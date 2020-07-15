from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from url_shortener.mixins import Timestamps
from .utils import encode_string
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

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = encode_string(self.user_url)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.user_url

    def get_short_url(self):
        return 'http://{}/{}'.format(getattr(settings, "DOMAIN_NAME"), self.url_hash)
