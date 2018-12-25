"""
Profile Model
"""

# Django
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )
    job_title = models.CharField(max_length=100, verbose_name="Job Title")
    company = models.CharField(max_length=100, verbose_name="Company")
    address = models.CharField(max_length=100, verbose_name="Address")
    github_url = models.CharField(max_length=100, verbose_name="Github URL")
    facebook_url = models.CharField(max_length=100, verbose_name="Facebook URL")
    twitter_url = models.CharField(max_length=100, verbose_name="Twitter URL")
    access_token = models.CharField(max_length=200, verbose_name="Access token")
    refresh_token = models.CharField(max_length=200, verbose_name="Refresh token")
    access_token_updated_at = models.DateTimeField(verbose_name="Access token last update", null=True)
    refresh_token_updated_at = models.DateTimeField(verbose_name="Refresh token last update", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
