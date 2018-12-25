"""
Task Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('failed', 'FAILED'),
        ('passed', 'PASSED'),
        ('error', 'ERROR')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user",
        null=True
    )
    uuid = models.CharField(max_length=200, verbose_name="UUID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Status")
    executor = models.CharField(max_length=200, verbose_name="Executor")
    parameters = models.TextField(verbose_name="Parameters")
    result = models.TextField(verbose_name="Result")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
