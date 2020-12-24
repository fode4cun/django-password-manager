from django.test import TestCase

from pwdgen.forms import GeneratorForm


class GeneratorFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'length_range': '15',
            'length_number': '15',
            'lowercase': ['on'],
            'uppercase': ['on'],
            'numbers': ['on'],
        }
        form = GeneratorForm(data=data)
        self.assertTrue(form.is_valid())

