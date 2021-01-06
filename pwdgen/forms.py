from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout
from django import forms

from pwdgen.generator import Generator
from pwdgen.models import Category, Password
from pwdgen.utils import encrypt_password

EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]


class GeneratorForm(forms.Form):
    pwd = forms.CharField(max_length=120, required=False, label='Password')
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
            Div('pwd', css_class='my-3'),
            Div('length_range', css_class='my-3'),
            Div('length_number', css_class='my-3')
        )

    def clean_pwd(self):
        return Generator(self.data).gen()


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name', 'url')

    def clean_name(self):
        name = self.cleaned_data['name']
        category = Category.objects.filter(owner=self.request.user, name=name).exists()
        if category:
            raise forms.ValidationError(f'The name {name} already exists')
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        name = self.cleaned_data['name']
        url = self.cleaned_data['url']

        if commit:
            instance.owner = self.request.user
            instance.name = name
            instance.url = url
            instance.save()
        return instance


class PasswordForm(forms.ModelForm):
    class Meta:
        model = Password
        fields = ('category', 'name', 'password')
        widgets = {
            'password': forms.TextInput(attrs={'type': 'hidden'})
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super().__init__(*args, **kwargs)
        if owner.is_authenticated:
            self.fields['category'].queryset = Category.objects.filter(owner=owner)

    def clean_name(self):
        name = self.cleaned_data['name']
        category = self.cleaned_data['category']
        password = Password.objects.filter(category=category, name=name).exists()
        if password:
            raise forms.ValidationError(f'The name {name} already exists')
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        category = self.cleaned_data['category']
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']
        crypted_pwd = encrypt_password(password)

        if commit:
            instance.category = category
            instance.name = name
            instance.password = crypted_pwd
            instance.save()

        return instance
