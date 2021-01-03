from shutil import rmtree

from django.conf import settings
from django.contrib.auth import get_user_model

from pwdgen.models import Category, Password
from pwdgen.utils import encrypt_password

TEST_MEDIA_PATH = str(settings.BASE_DIR.joinpath('test_media'))


class SetUpMixin:
    """
    Create Fixtures for testing.
    Login user for test.
    """

    def setUp(self):
        User = get_user_model()
        email = 'test@gmail.com'
        password = 'top_secret'

        self.crypted_pwd = encrypt_password('strong_password')
        self.user = User.objects.create_user(email=email, password=password)
        self.client.login(email=email, password=password)

        self.category = Category.objects.create(
            owner=self.user, name='Web', image='test.png')
        self.password = Password.objects.create(
            category=self.category, name='Gmail', password=self.crypted_pwd)

    def tearDown(self):
        rmtree(TEST_MEDIA_PATH)
