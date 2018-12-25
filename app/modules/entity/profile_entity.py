"""
User Entity Module
"""

# Django
from django.utils import timezone
from django.contrib.auth.models import User

# local Django
from app.models import Profile


class Profile_Entity():

    def profile_exists(self, user_id):
        try:
            user = Profile.objects.get(user=user_id)
            return False if user.pk is None else True
        except Exception:
            return False

    def create_profile(self, profile_data):

        if "user" not in profile_data:
            return False

        profile = Profile(
            job_title=profile_data["job_title"] if "job_title" in profile_data else "",
            company=profile_data["company"] if "company" in profile_data else "",
            address=profile_data["address"] if "address" in profile_data else "",
            github_url=profile_data["github_url"] if "github_url" in profile_data else "",
            facebook_url=profile_data["facebook_url"] if "facebook_url" in profile_data else "",
            twitter_url=profile_data["twitter_url"] if "twitter_url" in profile_data else "",
            access_token=profile_data["access_token"] if "access_token" in profile_data else "",
            refresh_token=profile_data["refresh_token"] if "refresh_token" in profile_data else "",
            access_token_updated_at=profile_data["access_token_updated_at"] if "access_token_updated_at" in profile_data else None,
            refresh_token_updated_at=profile_data["refresh_token_updated_at"] if "refresh_token_updated_at" in profile_data else None,
            user=User.objects.get(pk=profile_data["user"])
        )

        profile.save()
        return False if profile.pk is None else profile

    def update_profile(self, profile_data):

        if "user" not in profile_data:
            return False

        profile = self.get_profile_by_user_id(profile_data["user"])

        if profile is not False:

            if "job_title" in profile_data:
                profile.job_title = profile_data["job_title"]

            if "company" in profile_data:
                profile.company = profile_data["company"]

            if "address" in profile_data:
                profile.address = profile_data["address"]

            if "github_url" in profile_data:
                profile.github_url = profile_data["github_url"]

            if "facebook_url" in profile_data:
                profile.facebook_url = profile_data["facebook_url"]

            if "twitter_url" in profile_data:
                profile.twitter_url = profile_data["twitter_url"]

            if "access_token" in profile_data:
                profile.access_token = profile_data["access_token"]

            if "refresh_token" in profile_data:
                profile.refresh_token = profile_data["refresh_token"]

            if "access_token_updated_at" in profile_data:
                profile.access_token_updated_at = profile_data["access_token_updated_at"]

            if "refresh_token_updated_at" in profile_data:
                profile.refresh_token_updated_at = profile_data["refresh_token_updated_at"]

            profile.save()
            return True

    def get_profile_by_user_id(self, user_id):
        try:
            profile = Profile.objects.get(user=user_id)
            return False if profile.pk is None else profile
        except Exception:
            return False

    def get_profile_by_access_token(self, access_token):
        try:
            profile = Profile.objects.get(access_token=access_token)
            return False if profile.pk is None else profile
        except Exception:
            return False

    def get_profile_by_refresh_token(self, refresh_token):
        try:
            profile = Profile.objects.get(refresh_token=refresh_token)
            return False if profile.pk is None else profile
        except Exception:
            return False

    def token_used(self, token):
        try:
            profile = Profile.objects.get(Q(refresh_token=token) | Q(access_token=token))  # noqa: F821
            return False if profile.pk is None else True
        except Exception:
            return False

    def access_token_used(self, access_token):
        try:
            profile = Profile.objects.get(access_token=access_token)
            return False if profile.pk is None else True
        except Exception:
            return False

    def refresh_token_used(self, refresh_token):
        try:
            profile = Profile.objects.get(refresh_token=refresh_token)
            return False if profile.pk is None else True
        except Exception:
            return False

    def update_access_token(self, user_id, access_token):
        result = self.update_profile({
            "user": user_id,
            "access_token": access_token,
            "access_token_updated_at": timezone.now()
        })

        return result

    def update_refresh_token(self, user_id, refresh_token):
        result = self.update_profile({
            "user": user_id,
            "refresh_token": refresh_token,
            "refresh_token_updated_at": timezone.now()
        })

        return result

    def count_all_profiles(self):
        return Profile.objects.count()
