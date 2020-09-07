from django.test import TestCase, Client
from django.urls import reverse

from url_shortener.models import UrlStore
from url_shortener.utils import encode_string


class TestStringEncoder(TestCase):

    def test__utils_encode_string__on_int_input__should_return_true(self):
        return self.assertTrue(encode_string(11))

    def test__utils_encode_string__on_str_input__should_return_true(self):
        return self.assertTrue(encode_string('test'))

    def test__utils_encode_string__on_bool_input__should_return_true(self):
        return self.assertTrue(encode_string(True))

    def test__utils_encode_string__on_str_special_signs_input__should_return_true(self):
        return self.assertTrue(encode_string('@#$%%^&*('))

    def test__utils_encode_string__on_empty_list_input__raise_value_error(self):
        with self.assertRaises(ValueError):
            encode_string([])

    def test__utils_encode_string__on_empty_dict_input__raise_value_error(self):
        with self.assertRaises(ValueError):
            encode_string({})

    def test__utils_encode_string__on_empty_tuple_input__raise_value_error(self):
        with self.assertRaises(ValueError):
            encode_string(())

    def test__utils_encode_string__on_empty_string_input__should_raise_value_error(self):
        with self.assertRaises(ValueError):
            encode_string('')

    def test__utils_encode_string__on_size_equal_0__should_raise_value_error(self):
        with self.assertRaises(ValueError):
            encode_string('test', 0)

    def test__utils_encode_string__on_size_equal_None__should_raise_type_error(self):
        with self.assertRaises(TypeError):
            encode_string('test', None)

    def test__utils_encode_string__on_size_equal_some_str__should_raise_type_error(self):
        with self.assertRaises(TypeError):
            encode_string('test', 'test')

    def test__utils_encode_string__on_size_equal_10__should_return_hash_with_length_10(self):
        size_param = 10
        return self.assertEqual(len(encode_string('test', size_param)), size_param)

    def test__utils_encode_string__on_size_grater_than_128__should_raise_value_error(self):
        with self.assertRaises(ValueError):
            encode_string('test', 130)


class TestUrlView(TestCase):

    def setUp(self) -> None:
        """This method runs before the execution of each test case."""
        self.client = Client()
        self.url = reverse("home")

    def test__does_url_show_url_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.template_name[0], 'url_form.html')

    def test__is_provided_valid_url_in_post_response(self):
        data = {'user_url': "https://www.google.pl"}
        response = self.client.post(self.url, data)
        self.assertContains(response, data['user_url'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'url_form.html')

    def test__response_with_provided_invalid_url(self):
        data = {'user_url': "www.google.pl"}
        response = self.client.post(self.url, data)
        self.assertContains(response, "Enter a valid URL.")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'url_form.html')

    def test__is_provided_duplicated_valid_url_in_post_response(self):
        data = {'user_url': "https://www.google.pl"}
        self.client.post(self.url, data)
        second_response = self.client.post(self.url, data)
        self.assertContains(second_response, data['user_url'])
        self.assertContains(second_response, "Your provided URL already exist!")
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(second_response.template_name[0], 'url_form.html')
