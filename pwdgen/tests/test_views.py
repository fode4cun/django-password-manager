from django.test import TestCase
from django.urls import reverse

from pwdgen.forms import GeneratorForm


class HomeViewTest(TestCase):
    url = reverse('pwdgen:home')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], GeneratorForm)

    def test_post(self):
        data = {
            'length_range': '15',
            'length_number': '15',
            'lowercase': ['on'],
            'uppercase': ['on'],
            'numbers': ['on'],
        }

        response = self.client.post(self.url, data)
        password = response.context['form']['password'].value()
        length = int(data['length_range'])

        self.assertRegex(password, r'(?=.*[a-z])')
        self.assertRegex(password, r'(?=.*[A-Z])')
        self.assertRegex(password, r'(?=.*[0-9])')
        self.assertEqual(len(password), length)

