"""
Incident Model
"""

# Third Party Library
from django.db import models


class Incident(models.Model):

    STATUS_CHOICES = (
        ('open', 'OPEN'),
        ('closed', 'CLOSED')
    )

    name = models.CharField(max_length=200, verbose_name="Name")
    uri = models.CharField(max_length=50, verbose_name="URI", unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open", verbose_name="Status")
    datetime = models.DateTimeField(verbose_name="Datetime")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
