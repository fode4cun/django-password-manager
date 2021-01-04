from django.test import SimpleTestCase, TestCase, tag
from django.urls import reverse

from pwdgen.forms import GeneratorForm

DATA = {
    'length_range': '15',
    'length_number': '15',
    'lowercase': ['on'],
    'uppercase': ['on'],
    'numbers': ['on'],
}


@tag('home')
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


@tag('generator-form')
class GeneratorFormTest(TestCase):
    def test_valid_form(self):
        form = GeneratorForm(data=DATA)

        self.assertTrue(form.is_valid())


@tag('error-handler')
class CustomErrorHandlerTests(SimpleTestCase):
    def test_handler_400(self):
        response = self.client.get('/400/')

        self.assertContains(response, 'Bad Request', status_code=400)

    def test_handler_403(self):
        response = self.client.get('/403/')

        self.assertContains(response, 'Access Denied', status_code=403)

    def test_handler_404(self):
        response = self.client.get('/404/')

        self.assertContains(response, 'Page Not Found', status_code=404)

    def test_handler_500(self):
        response = self.client.get('/500/')

        self.assertContains(response, 'Internal Server Error', status_code=500)
