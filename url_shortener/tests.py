from django.core.exceptions import ValidationError
from django.test import TestCase


class TestUrlValidator(TestCase):

    def test__url_validator__should_return_true(self):
        from .validators import validate_url

        test_urls = [
            'http://www.google.pl',
            'http://www.google.com',
            'http://dev.google.com',
            'http://google.com',
            'http://www.google.com/abc',
            'http://www.google.com/abc.html',
            'http://www.google.com/abc#def',
            'http://www.google.com/abc/111#def',
            'https://www.google.pl',
            'https://www.google.com',
            'https://dev.google.com',
            'https://google.com',
            'https://www.google.com/abc',
            'https://www.google.com/abc.html',
            'https://www.google.com/abc#def',
            'https://www.google.com/abc/111#def',
        ]
        for url in test_urls:
            url = validate_url(url)
            self.assertTrue(url)

    def test__url_validator__should_raise_validation_error(self):
        from .validators import validate_url

        test_urls = [
            'http://www.google.com@aaa/abc#def',
            'https://www.google.com@aaa/abc#def',
            'http//www.google.pl',
            'http:/www.google.pl',
            'http:/www.google.paaaal',
            'http:/www.google.pl/@#aa',
            'http:/wwwgoogle.pl',
            'http:/www.googlepl',
            'google.pl',
            'dev.google.com',
            'www.google.pl',
            'www.google.com',
            'www.google.com/abc',
            'www.google.com/abc.html',
            'www.google.com/abc#def',
            'www.google.com@aaa/abc#def',
            'www.google.com/abc/111#def',
        ]
        for url in test_urls:
            with self.assertRaises(ValidationError):
                validate_url(url)
