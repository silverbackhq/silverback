"""
Metric Entity Module
"""

from app.models import Metric


class Metric_Entity():

    def insert_one(self, metric):

        new_metric = Metric()

        if "title" in metric:
            new_metric.title = metric["title"]

        if "description" in metric:
            new_metric.description = metric["description"]

        if "source" in metric:
            new_metric.source = metric["source"]

        if "data" in metric:
            new_metric.data = metric["data"]

        new_metric.save()
        return False if new_metric.pk is None else new_metric

    def update_one_by_id(self, id, metric_data):
        metric = self.get_one_by_id(id)

        if metric is not False:
            if "title" in metric_data:
                metric.title = metric_data["title"]

            if "description" in metric_data:
                metric.description = metric_data["description"]

            if "source" in metric_data:
                metric.source = metric_data["source"]

            if "data" in metric_data:
                metric.data = metric_data["data"]

            metric.save()
            return True
        return False

    def count_all(self):
        return Metric.objects.count()

    def get_all(self, offset=None, limit=None):
        if offset is None or limit is None:
            return Metric.objects.order_by('-created_at')

        return Metric.objects.order_by('-created_at')[offset:limit+offset]

    def get_one_by_id(self, metric_id):
        try:
            metric = Metric.objects.get(id=metric_id)
            return False if metric.pk is None else metric
        except Exception:
            return False

    def delete_one_by_id(self, id):
        metric = self.get_one_by_id(id)
        if metric is not False:
            count, deleted = metric.delete()
            return True if count > 0 else False
        return False
