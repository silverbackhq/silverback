"""
Incident Update Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User

# local Django
from .incident import Incident


class Incident_Update(models.Model):

    STATUS_CHOICES = (
        ('Investigating', 'INVESTIGATING'),
        ('Identified', 'IDENTIFIED'),
        ('Monitoring', 'MONITORING'),
        ('Update', 'UPDATE'),
        ('Resolved', 'RESOLVED')
    )

    NOTIFY_CHOICES = (
        ('on', 'ON'),
        ('off', 'OFF')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Incident",
        null=True
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open", verbose_name="Status")
    notify_subscribers = models.CharField(max_length=50, choices=NOTIFY_CHOICES, default="on", verbose_name="Notify Subscribers")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Time")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")