# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Third Party Library
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

    class Meta:
        db_table = "app_profile"
