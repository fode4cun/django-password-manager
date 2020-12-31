from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from pwdgen.forms import GeneratorForm

User = get_user_model()
TEST_MEDIA_PATH = str(settings.BASE_DIR.joinpath('test_media'))


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


class CategoryFormViewTest(TestCase):
    url = reverse('pwdgen:category-create')

    @override_settings(MEDIA_ROOT=TEST_MEDIA_PATH)
    def test_post(self):
        data = {
            'name': 'Python',
            'url': 'https://image.flaticon.com/icons/png/128/3098/3098090.png',
        }
        email = 'test@gmail.com'
        password = 'top_secret'

        user = User.objects.create_user(email=email, password=password)
        self.client.login(email=email, password=password)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)


class SearchIconViewTest(TestCase):
    url = reverse('pwdgen:search-icon')

    def test_get(self):
        parameter = {'word': 'python'}
        response = self.client.get(self.url, parameter)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        items = response.json()
        self.assertNotEqual(len(items['results']), 0)

