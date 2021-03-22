from django.contrib.auth import get_user_model
from django.db import models
from django.urls.base import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from layout.models import CreationModificationDateBase


class Category(CreationModificationDateBase):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=64)
    slug = models.CharField(max_length=128)
    url = models.URLField()

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['-created']
        unique_together = [['owner', 'name']]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pwdgen:category-list')

    def __str__(self):
        return self.name


class Password(CreationModificationDateBase):
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
        related_name='categories',
    )
    name = models.CharField(_('Name'), max_length=64)
    slug = models.CharField(max_length=128)
    password = models.CharField(_('Password'), max_length=255)

    class Meta:
        get_latest_by = '-created'
        verbose_name = _('Password')
        verbose_name_plural = _('Passwords')
        ordering = ['-created']
        unique_together = [['category', 'name']]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pwdgen:category-detail', args=[str(self.category.slug)])

    def __str__(self):
        return self.name
