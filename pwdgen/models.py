from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _

from layout.models import CommonFieldsBase, CreationModificationDateBase


def upload_to(instance, filename):
    now = timezone_now()
    return f"category/{now:%Y/%m}/{filename}"


class Category(CommonFieldsBase, CreationModificationDateBase):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    slug = models.CharField(max_length=128)
    image = models.ImageField(upload_to=upload_to)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['-created']
        unique_together = [['owner', 'name']]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.storage.delete(self.image.name)
        return super().delete(*args, **kwargs)


class Password(CommonFieldsBase, CreationModificationDateBase):
    category = models.ForeignKey(
        'Category',
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
        related_name='categories',
    )
    password = models.CharField(_('Password'), max_length=255)

    class Meta:
        verbose_name = _('Password')
        verbose_name_plural = ('Passwords')
        ordering = ['-created']

