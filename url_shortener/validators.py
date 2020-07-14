from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator


def validate_url(url):
    REGEX = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    url_validator = URLValidator()
    regex_url_validator = RegexValidator(regex=REGEX)
    try:
        url_validator(url)
        regex_url_validator(url)
    except Exception:
        raise ValidationError("Invalid URL")
    return url
