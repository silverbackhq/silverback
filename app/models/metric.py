"""
Metric Model
"""

# Django
from django.db import models


class Metric(models.Model):

    TYPE_CHOICES = (
        ('graphite', 'GRAPHITE'),
        ('prometheus', 'PROMETHEUS')
    )

    title = models.CharField(max_length=200, verbose_name="Title")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="graphite", verbose_name="Type")
    source = models.TextField(verbose_name="Source")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
