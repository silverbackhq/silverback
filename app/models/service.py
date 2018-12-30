"""
Service Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):

    UPTIME_CHOICES = (
        ('on', 'ON'),
        ('off', 'OFF')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )

    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.CharField(max_length=200, verbose_name="Description")
    uptime = models.CharField(max_length=50, choices=UPTIME_CHOICES, default="off", verbose_name="Uptime")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
