"""
    Activity Model
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related User"
    )

    activity = models.TextField(verbose_name="Activity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_activity"
