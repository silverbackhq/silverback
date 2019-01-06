"""
Activity Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )

    activity = models.TextField(verbose_name="Activity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
