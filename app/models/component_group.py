"""
Component Model
"""

# Django
from django.db import models


class Component_Group(models.Model):

    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.CharField(max_length=200, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
