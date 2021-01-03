from django.test import TestCase, override_settings, tag
from django.urls import reverse

from pwdgen.tests.mixins import TEST_MEDIA_PATH, SetUpMixin
from pwdgen.utils import decrypt_password


@tag('category-form')
class CategoryFormTest(SetUpMixin, TestCase):
    url = reverse('pwdgen:category-create')

    @override_settings(MEDIA_ROOT=TEST_MEDIA_PATH)
    def test_valid_post(self):
        data = {
            'name': 'Python',
            'url': 'https://image.flaticon.com/icons/png/128/3098/3098090.png',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_PATH)
    def test_invalid_post(self):
        data = {
            'name': 'Web',
            'url': 'https://image.flaticon.com/icons/png/128/3098/3098090.png',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', f'The name {data["name"]} already exists')


@tag('password-form')
class PasswordFormTest(SetUpMixin, TestCase):
    url = reverse('pwdgen:password-save')

    def test_valid_post(self):
        decrypted_pwd = decrypt_password(self.crypted_pwd)
        data = {
            'category': str(self.category.pk),
            'name': 'Python',
            'password': 'strong_password'
        }
        response = self.client.post(self.url, data)

        self.assertNotEqual(self.crypted_pwd, 'strong_password')
        self.assertEqual(decrypted_pwd, 'strong_password')
        self.assertEqual(response.status_code, 302)

    def test_invalid_post(self):
        data = {
            'category': str(self.category.pk),
            'name': 'Gmail',
            'password': 'strong_password'
        }
        response = self.client.post(self.url, data)
        error = response.json()['name']

        self.assertEqual(response.status_code, 400)
        self.assertEqual(error, [f'The name {data["name"]} already exists'])

    def test_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)
