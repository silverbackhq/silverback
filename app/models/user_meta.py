"""
    User Meta Model
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.db import models
from django.contrib.auth.models import User


class UserMeta(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related User"
    )

    key = models.CharField(max_length=30, db_index=True, verbose_name="Meta key")
    value = models.CharField(max_length=200, verbose_name="Meta value")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return self.key

    class Meta:
        db_table = "app_user_meta"
