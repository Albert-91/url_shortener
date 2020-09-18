from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.urls import reverse

from .utils import encode_string


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

    @classmethod
    def setUpClass(cls):
        cls.host = "localhost"
        cls.port = 8000
        super().setUpClass()

    def setUp(self) -> None:
        """This method runs before the execution of each test case."""
        self.client = Client()
        self.url = reverse("home")

    def test__does_url_show_url_form_template(self):
        response = self.client.get(self.url)
        with self.assertTemplateUsed(template_name='url_form.html'):
            render_to_string(response.template_name[0])

    def test__status_code_for_valid_url__should_return_200(self):
        data = {'user_url': "https://www.google.pl"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test__provided_valid_url_in_response__should_be_in_html_response(self):
        data = {'user_url': "https://www.google.pl"}
        response = self.client.post(self.url, data)
        self.assertContains(response, data['user_url'])

    def test__template_after_provided_valid_url_in_response__should_return_url_form(self):
        data = {'user_url': "https://www.google.pl"}
        response = self.client.post(self.url, data)
        with self.assertTemplateUsed(template_name='url_form.html'):
            render_to_string(response.template_name[0])

    def test__context_data_from_provided_valid_url_in_response__should_be_in_html_response(self):
        data = {'user_url': "https://www.google.pl"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.context_data['is_created'], True)
        self.assertEqual(response.context_data['url'].user_url, data['user_url'])

    def test__status_code_for_invalid_url__should_return_200(self):
        data = {'user_url': "www.google.pl"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test__template_after_provided_invalid_url_in_response__should_return_url_form(self):
        data = {'user_url': "www.google.pl"}
        response = self.client.post(self.url, data)
        with self.assertTemplateUsed(template_name='url_form.html'):
            render_to_string(response.template_name[0])

    def test__response_with_provided_invalid_url__should_contains_info_to_enter_valid_url(self):
        data = {'user_url': "www.google.pl"}
        response = self.client.post(self.url, data)
        self.assertContains(response, "Enter a valid URL.")

    def test__response_after_provided_duplicated_valid_url__should_contains_info_that_url_already_exist(self):
        data = {'user_url': "https://www.google.pl"}
        self.client.post(self.url, data)
        second_response = self.client.post(self.url, data)
        self.assertContains(second_response, "Your provided URL already exist!")

    def test__response_status_code_after_provided_duplicated_valid_url__should_return_200(self):
        data = {'user_url': "https://www.google.pl"}
        self.client.post(self.url, data)
        second_response = self.client.post(self.url, data)
        self.assertEqual(second_response.status_code, 200)

    def test__template_of_response_after_provided_duplicated_valid_url__should_return_url_form(self):
        data = {'user_url': "https://www.google.pl"}
        self.client.post(self.url, data)
        second_response = self.client.post(self.url, data)
        with self.assertTemplateUsed(template_name='url_form.html'):
            render_to_string(second_response.template_name[0])

    def test__response_of_shortened_url__should_return_redirect_chain_to_original_url(self):
        data = {'user_url': "https://www.google.pl"}
        short_url = self.client.post(self.url, data).context_data['short_url']
        response = self.client.get(short_url, follow=True)
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertIn(response.redirect_chain[0][0], short_url + '/')
        self.assertEqual(response.redirect_chain[1][0], data['user_url'])
