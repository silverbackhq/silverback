"""
Component Model
"""

# Third Party Library
from django.db import models

# Local Library
from .component_group import ComponentGroup


class Component(models.Model):

    UPTIME_CHOICES = (
        ('on', 'ON'),
        ('off', 'OFF')
    )

    group = models.ForeignKey(
        ComponentGroup,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Component Group",
        null=True
    )

    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.CharField(max_length=200, verbose_name="Description")
    uptime = models.CharField(max_length=50, choices=UPTIME_CHOICES, default="off", verbose_name="Uptime")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_component"
