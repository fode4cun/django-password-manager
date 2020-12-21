from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.text import slugify

from pwdgen.models import Category


class CategoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        self.category = Category.objects.create(
            owner=self.user, name='Web Pages')

    def test_category_creation(self):
        category = self.category
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.slug, slugify(category.name))
        self.assertEqual(category.__str__(), category.name)

