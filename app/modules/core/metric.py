"""
Metric Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.metric_entity import Metric_Entity


class Metric():

    __metric_entity = None
    __helpers = None
    __logger = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__metric_entity = Metric_Entity()
        self.__logger = self.__helpers.get_logger(__name__)

    def get_one_by_id(self, id):
        metric = self.__metric_entity.get_one_by_id(id)

        if not metric:
            return False

        return {
            "id": metric.id,
            "title": metric.title,
            "type": metric.type,
            "source": metric.source
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
