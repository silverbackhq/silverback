"""
Incident Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User


class Incident(models.Model):

    STATUS_CHOICES = (
        ('open', 'OPEN'),
        ('closed', 'CLOSED')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )

    name = models.CharField(max_length=200, verbose_name="Name")
    uri = models.CharField(max_length=50, verbose_name="URI", unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open", verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
