"""
User Meta Model
"""

# Django
from django.db import models


class Reset_Request(models.Model):

    email = models.CharField(max_length=100, db_index=True, verbose_name="Email")
    token = models.CharField(max_length=200, db_index=True, verbose_name="Token")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    expire_at = models.DateTimeField(verbose_name="Expire at")
    messages_count = models.PositiveSmallIntegerField(verbose_name="Messages Count")
