"""
Notification Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User

# local Django
from .task import Task


class Notification(models.Model):

    TYPE_CHOICES = (
        ('pending', 'PENDING'),
        ('failed', 'FAILED'),
        ('passed', 'PASSED'),
        ('error', 'ERROR'),
        ('message', 'MESSAGE')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Task",
        null=True
    )

    highlight = models.CharField(max_length=200, verbose_name="Highlight")
    notification = models.CharField(max_length=200, verbose_name="Notification")
    url = models.CharField(max_length=200, verbose_name="URL")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="message", verbose_name="Type")
    delivered = models.BooleanField(default=False, verbose_name="Delivered")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
