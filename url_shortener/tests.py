from django.test import TestCase

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
