import os
from hashlib import blake2b
from typing import Text

from django.conf import settings


def encode_string(s: Text) -> Text:
    salt = os.urandom(blake2b.SALT_SIZE)
    return blake2b(bytes(str(s), encoding='utf-8'),
                   digest_size=getattr(settings, "SHORT_URL_DEFAULT_LENGTH", 10),
                   salt=salt).hexdigest()
