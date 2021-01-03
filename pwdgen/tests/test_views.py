from django.test import TestCase, override_settings, tag
from django.urls import reverse

from pwdgen.forms import CategoryForm
from pwdgen.tests.mixins import TEST_MEDIA_PATH, SetUpMixin


@tag('category-detail')
class CategoryDetailViewTest(SetUpMixin, TestCase):
    def test_logged_in_get(self):
        response = self.client.get(
            reverse('pwdgen:category-detail', args=[self.category.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.context['pwd_qs']), 0)

    def test_logged_out_get(self):
        self.client.logout()
        response = self.client.get(
            reverse('pwdgen:category-detail', args=[self.category.slug])
        )

        self.assertEqual(response.status_code, 302)


@tag('category-edit')
class CategoryEditViewTest(SetUpMixin, TestCase):
    def test_get(self):
        response = self.client.get(
            reverse('pwdgen:category-edit', args=[self.category.slug])
        )
        category_form = response.context['form']

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(category_form, CategoryForm)
        self.assertEqual(category_form['url'].initial, 'Image already exists')


@tag('category-delete')
class CategoryDeleteView(SetUpMixin, TestCase):
    def test_get(self):
        response = self.client.get(
            reverse('pwdgen:category-delete', args=[self.category.slug])
        )

        self.assertEqual(response.status_code, 200)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_PATH)
    def test_post(self):
        response = self.client.post(
            reverse('pwdgen:category-delete', args=[self.category.slug])
        )

        self.assertEqual(response.status_code, 302)


@tag('password-delete')
class PasswordDeleteView(SetUpMixin, TestCase):
    def test_post(self):
        response = self.client.post(
            reverse('pwdgen:password-delete', kwargs={'category_slug': self.category.slug, 'pwd_slug': self.password.slug})
        )

        self.assertEqual(response.status_code, 302)


@tag('search-icon')
class SearchIconViewTest(SetUpMixin, TestCase):
    def test_get(self):
        parameter = {'word': 'python'}
        response = self.client.get(reverse('pwdgen:search-icon'), parameter)
        items = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertNotEqual(len(items['results']), 0)
