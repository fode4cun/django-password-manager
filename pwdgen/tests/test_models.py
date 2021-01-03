from django.test import TestCase, tag
from django.utils.text import slugify

from pwdgen.models import Category, Password
from pwdgen.tests.mixins import SetUpMixin


@tag('models')
class ModelsTest(SetUpMixin, TestCase):
    def test_category_creation(self):
        category = self.category

        self.assertIsInstance(category, Category)
        self.assertEqual(category.slug, slugify(category.name))
        self.assertEqual(category.__str__(), category.name)

    def test_password_creation(self):
        password = self.password

        self.assertIsInstance(password, Password)
        self.assertEqual(password.slug, slugify(password.name))
        self.assertEqual(password.__str__(), password.name)
