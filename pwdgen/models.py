from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from layout.models import CommonFieldsBase, CreationModificationDateBase


class Category(CommonFieldsBase, CreationModificationDateBase):
    slug = models.CharField(max_length=128)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['-created']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)


class Repository(CommonFieldsBase, CreationModificationDateBase):
    category = models.ForeignKey(
        'Category',
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
        related_name='categories',
    )
    password = models.CharField(_('Password'), max_length=255)

    class Meta:
        verbose_name = _('Repository')
        verbose_name_plural = ('Repositories')
        ordering = ['-created']

