from django.test import TestCase
from django.urls import reverse

from pwdgen.forms import GeneratorForm

DATA = {
    'length_range': '15',
    'length_number': '15',
    'lowercase': ['on'],
    'uppercase': ['on'],
    'numbers': ['on'],
}


class HomeViewTest(TestCase):
    url = reverse('layout:home')

    def test_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], GeneratorForm)

    def test_post(self):
        response = self.client.post(self.url, DATA)
        password = response.context['form']['pwd'].value()
        length = int(DATA['length_range'])

        self.assertRegex(password, r'(?=.*[a-z])')
        self.assertRegex(password, r'(?=.*[A-Z])')
        self.assertRegex(password, r'(?=.*[0-9])')
        self.assertEqual(len(password), length)


class GeneratorFormTest(TestCase):
    def test_valid_form(self):
        form = GeneratorForm(data=DATA)

        self.assertTrue(form.is_valid())
