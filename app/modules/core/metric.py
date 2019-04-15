"""
Metric Module
"""

from pyumetric import NewRelic_Provider
from app.modules.entity.metric_entity import Metric_Entity
from app.modules.entity.option_entity import Option_Entity


class Metric():

    __metric_entity = None
    __option_entity = None
    __newrelic = None

    def __init__(self):
        self.__option_entity = Option_Entity()
        self.__metric_entity = Metric_Entity()
        new_relic_api = self.__option_entity.get_one_by_key("newrelic_api_key")
        if new_relic_api:
            self.__newrelic = NewRelic_Provider(new_relic_api.value)

    def get_one_by_id(self, id):
        metric = self.__metric_entity.get_one_by_id(id)

        if not metric:
            return False

        return {
            "id": metric.id,
            "title": metric.title,
            "description": metric.description,
            "source": metric.source,
            "data": metric.data,
            "x_axis": metric.x_axis,
            "y_axis": metric.y_axis
        }

    def insert_one(self, metric):
        return self.__metric_entity.insert_one(metric)

    def update_one_by_id(self, id, metric_data):
        return self.__metric_entity.update_one_by_id(id, metric_data)

    def count_all(self):
        return self.__metric_entity.count_all()

    def get_all(self, offset=None, limit=None):
        return self.__metric_entity.get_all(offset, limit)

    def delete_one_by_id(self, id):
        return self.__metric_entity.delete_one_by_id(id)

    def get_new_relic_apps(self):
        result = []
        try:
            apps = self.__newrelic.get_apps().json()
            for app in apps["applications"]:
                result.append({"key": app["id"], "value": app["name"]})
            return result
        except Exception:
            return False
