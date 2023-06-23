from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _('Ekleme Tarihi'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Güncelleme Tarihi'),
        null=True,
        blank=True,
        auto_now=True
    )

    class Meta:
        abstract = True
