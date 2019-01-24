"""
Subscriber Entity Module
"""

from app.models import Subscriber


class Subscriber_Entity():

    def insert_one(self, subscriber):

        new_subscriber = Subscriber()

        if "email" in subscriber:
            new_subscriber.email = subscriber["email"]

        if "phone" in subscriber:
            new_subscriber.phone = subscriber["phone"]

        if "endpoint" in subscriber:
            new_subscriber.endpoint = subscriber["endpoint"]

        if "auth_token" in subscriber:
            new_subscriber.auth_token = subscriber["auth_token"]

        if "type" in subscriber:
            new_subscriber.type = subscriber["type"]

        if "status" in subscriber:
            new_subscriber.status = subscriber["status"]

        if "external_id" in subscriber:
            new_subscriber.external_id = subscriber["external_id"]

        new_subscriber.save()
        return False if new_subscriber.pk is None else new_subscriber

    def update_one_by_id(self, id, subscriber_data):
        subscriber = self.get_one_by_id(id)

        if subscriber is not False:

            if "email" in subscriber_data:
                subscriber.email = subscriber_data["email"]

            if "phone" in subscriber_data:
                subscriber.phone = subscriber_data["phone"]

            if "endpoint" in subscriber_data:
                subscriber.endpoint = subscriber_data["endpoint"]

            if "auth_token" in subscriber_data:
                subscriber.auth_token = subscriber_data["auth_token"]

            if "type" in subscriber_data:
                subscriber.type = subscriber_data["type"]

            if "status" in subscriber_data:
                subscriber.status = subscriber_data["status"]

            if "external_id" in subscriber_data:
                subscriber.external_id = subscriber_data["external_id"]

            subscriber.save()
            return True
        return False

    def count_all(self):
        return Subscriber.objects.count()

    def count_by_status(self, status):
        return Subscriber.objects.filter(status=status).count()

    def get_all(self, offset=None, limit=None):
        if offset is None or limit is None:
            return Subscriber.objects.order_by('-created_at').get()

        return Subscriber.objects.order_by('-created_at')[offset:limit+offset]

    def get_iterator(self, status="verified"):
        return Subscriber.objects.filter(status=status).iterator()

    def get_one_by_id(self, subscriber_id):
        try:
            subscriber = Subscriber.objects.get(id=subscriber_id)
            return False if subscriber.pk is None else subscriber
        except Exception:
            return False

    def get_one_by_external_id(self, external_id):
        try:
            subscriber = Subscriber.objects.get(external_id=external_id)
            return False if subscriber.pk is None else subscriber
        except Exception:
            return False

    def delete_one_by_id(self, id):
        subscriber = self.get_one_by_id(id)
        if subscriber is not False:
            count, deleted = subscriber.delete()
            return True if count > 0 else False
        return False
