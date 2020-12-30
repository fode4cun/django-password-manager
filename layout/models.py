from django.db import models
from django.utils.translation import gettext_lazy as _


class CommonFieldsBase(models.Model):
    """
    Abstract base class with common fields
    :owner: - relation to current user.
    :name: - required / unique.
    """

    name = models.CharField(_('Name'), max_length=64)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CreationModificationDateBase(models.Model):
    """
    Abstract base class with a creation and modification date and time
    """

    created = models.DateTimeField(
        _("Creation Date and Time"),
        auto_now_add=True,
    )

    modified = models.DateTimeField(
        _("Modification Date and Time"),
        auto_now=True,
    )

    class Meta:
        abstract = True

