"""
    Metric Model
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.db import models


class Metric(models.Model):

    SOURCE_CHOICES = (
        ('newrelic', 'NEW_RELIC'),
        ('librato', 'LIBRATO'),
        ('datadog', 'DATADOG'),
        ('pingdom', 'PINGDOM')
    )

    title = models.CharField(max_length=150, verbose_name="Title")
    description = models.CharField(max_length=200, verbose_name="Description")
    x_axis = models.CharField(max_length=100, verbose_name="x_axis")
    y_axis = models.CharField(max_length=100, verbose_name="y_axis")
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default="newrelic", verbose_name="Source")
    data = models.TextField(verbose_name="Data")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_metric"
