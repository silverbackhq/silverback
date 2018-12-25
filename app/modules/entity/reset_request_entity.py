"""
Reset Request Entity Module
"""

# standard library
from datetime import datetime
from datetime import timedelta

# Django
from django.utils import timezone
from django.utils.crypto import get_random_string

# local Django
from app.models import Reset_Request


class Reset_Request_Entity():

    def gererate_token(self):
        """Generate a Token"""
        token = get_random_string(length=50)
        while self.get_one_by_token(token) is not False:
            token = get_random_string(length=50)
        return token

    def insert_one(self, request):
        """Insert a New Reset Request"""
        if self.get_one_by_email(request["email"]) is not False:
            return False

        request = Reset_Request(
            email=request["email"],
            token=request["token"] if "token" in request else self.gererate_token(),
            expire_at=request["expire_at"] if "expire_at" in request else timezone.now() + timedelta(hours=int(request["expire_after"])),
            messages_count=request["messages_count"]
        )

        request.save()
        return False if request.pk is None else request

    def insert_many(self, requests):
        """Insert Many Reset Requests"""
        status = True
        for request in requests:
            status &= True if self.insert_one(request) is not False else False
        return status

    def get_one_by_id(self, id):
        """Get Reset Request By ID"""
        try:
            reset_request = Reset_Request.objects.get(pk=id)
            return False if reset_request.pk is None else reset_request
        except Exception:
            return False

    def get_one_by_email(self, email):
        """Get Reset Request By Email"""
        try:
            reset_request = Reset_Request.objects.get(email=email)
            return False if reset_request.pk is None else reset_request
        except Exception:
            return False

    def get_one_by_token(self, token):
        """Get Reset Request By Token"""
        try:
            reset_request = Reset_Request.objects.get(token=token)
            return False if reset_request.pk is None else reset_request
        except Exception:
            return False

    def clear_expired_tokens(self):
        """Clear all Expired Tokens"""
        Reset_Request.objects.filter(expire_at__lt=datetime.now()).delete()

    def delete_one_by_id(self, id):
        """Delete Reset Request By ID"""
        request = self.get_one_by_id(id)
        if request is not False:
            count, deleted = request.delete()
            return True if count > 0 else False
        return False

    def delete_one_by_token(self, token):
        """Delete Reset Request By Token"""
        request = self.get_one_by_token(token)
        if request is not False:
            count, deleted = request.delete()
            return True if count > 0 else False
        return False

    def delete_one_by_email(self, email):
        """Delete Reset Request By Email"""
        request = self.get_one_by_email(email)
        if request is not False:
            count, deleted = request.delete()
            return True if count > 0 else False
        return False
