"""
Option Model
"""

# Django
from django.db import models


class Option(models.Model):

    key = models.CharField(max_length=30, db_index=True, verbose_name="Key")
    value = models.CharField(max_length=200, verbose_name="Value")
    autoload = models.BooleanField(default=False, verbose_name="Autoload")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
