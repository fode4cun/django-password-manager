from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms
from django.utils.translation import gettext_lazy as _
from PIL import Image

from pwdgen.generator import Generator
from pwdgen.models import Category
from pwdgen.utils import pil_to_django, retrieve_image


class GeneratorForm(forms.Form):
    password = forms.CharField(max_length=120, required=False)
    length_range = forms.IntegerField(
        min_value=12,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'value': '12',
            'oninput': 'this.form.length_number.value=this.value',
        })
    )
    length_number = forms.IntegerField(
        min_value=12,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'value': '12',
            'oninput': 'this.form.length_range.value=this.value',
        })
    )
    lowercase = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    uppercase = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    punctuation = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    numbers = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('password', css_class='my-3'),
            Div('length_range', css_class='my-3'),
            Div('length_number', css_class='my-3')
        )

    def clean_password(self):
        return Generator(self.data).gen()


class CategoryForm(forms.ModelForm):
    url = forms.CharField(
        max_length=120,
        required=True,
        label='image url'
    )

    class Meta:
        model = Category
        fields = ('name', 'url')

    def clean(self):
        return super().clean()

    def save(self, request, commit=True):
        instance = super().save(commit=False)
        name = self.cleaned_data['name']
        url = self.cleaned_data['url']

        file_stream = retrieve_image(url)
        pil_image = Image.open(file_stream)
        file_obj = pil_to_django(pil_image)
        instance.image.save(url, file_obj, save=False)

        if commit:
            instance.owner = request.user
            instance.name = name
            instance.save()
        return instance
