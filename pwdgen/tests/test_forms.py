from django.test import TestCase
from django.urls.base import reverse

from pwdgen.forms import GeneratorForm, CategoryForm


class GeneratorFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'length_range': '15',
            'length_number': '15',
            'lowercase': ['on'],
            'uppercase': ['on'],
            'numbers': ['on'],
        }
        form = GeneratorForm(data=data)
        self.assertTrue(form.is_valid())


class CategoryFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'name': 'Python',
            'url': 'https://image.flaticon.com/icons/png/128/3098/3098090.png',
        }
        form = CategoryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'name': 'Python',
            'url': '',
        }
        form = CategoryForm(data=data)
        self.assertEqual(form.errors['url'], ['This field is required.'])
