from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import slugify

from pwdgen.models import Category

User = get_user_model()


class CategoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='jacob@gmail.com', password='top_secret')
        self.category = Category.objects.create(
            owner=self.user, name='Web Pages')

    def test_category_creation(self):
        category = self.category
        self.assertIsInstance(category, Category)
        self.assertEqual(category.slug, slugify(category.name))
        self.assertEqual(category.__str__(), category.name)
