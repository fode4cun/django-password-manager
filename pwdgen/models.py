from django.db import models
from django.utils.text import slugify

from layout.models import CommonFieldsBase, CreationModificationDateBase


class Category(CommonFieldsBase, CreationModificationDateBase):
    slug = models.CharField(max_length=128)

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)


class Repository(CommonFieldsBase, CreationModificationDateBase):
    category = models.ForeignKey(
        'Category',
        verbose_name=('Category'),
        on_delete=models.CASCADE,
        related_name='categories',
    )
    password = models.CharField(('Password'), max_length=255)

    class Meta:
        verbose_name = ('Repository')
        verbose_name_plural = ('Repositories')
        ordering = ['-created']

