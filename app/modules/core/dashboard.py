"""
Dashboard Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.incident_entity import Incident_Entity
from app.modules.entity.incident_update_entity import Incident_Update_Entity
from app.modules.entity.incident_update_component_entity import Incident_Update_Component_Entity
from app.modules.entity.incident_update_notification_entity import Incident_Update_Notification_Entity
from app.modules.entity.subscriber_entity import Subscriber_Entity
from app.modules.entity.user_entity import User_Entity
from app.modules.entity.component_entity import Component_Entity
from app.modules.entity.component_group_entity import Component_Group_Entity
from app.modules.entity.metric_entity import Metric_Entity


class Dashboard():

    __helpers = None
    __logger = None
    __incident = None
    __incident_update = None
    __incident_update_component = None
    __incident_update_notification = None
    __subscriber = None
    __user = None
    __component = None
    __component_group = None
    __metric = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def incidents_count(self):
        return 20

    def subscribers_count(self):
        return 20

    def components_count(self):
        return 20

    def component_groups_count(self):
        return 20

    def metrics_count(self):
        return 20

    def users_count(self):
        return 20

    def delivered_notifications_count(self):
        return 20

    def failed_notifications_count(self):
        return 20

    def subscribers_chart(self):
        return ", ".join(str(x) for x in [0, 5, 1, 2, 7, 5, 6, 8, 24, 7, 12, 5, 6, 3, 2, 2, 6, 30, 10, 10, 15, 14, 47, 65, 55])

    def components_chart(self):
        return ", ".join(str(x) for x in [0, 5, 1, 2, 7, 5, 6, 8, 24, 7, 12, 5, 6, 3, 2, 2, 6, 30, 10, 10, 15, 14, 47, 65, 55])

    def delivered_notifications_chart(self):
        return ", ".join(str(x) for x in [0, 5, 1, 2, 7, 5, 6, 8, 24, 7, 12, 5, 6, 3, 2, 2, 6, 30, 10, 10, 15, 14, 47, 65, 55])

    def failed_notifications_chart(self):
        return ", ".join(str(x) for x in [0, 5, 1, 2, 7, 5, 6, 8, 24, 7, 12, 5, 6, 3, 2, 2, 6, 30, 10, 10, 15, 14, 47, 65, 55])

    def incidents_chart(self):
        return ", ".join(str(x) for x in [0, 5, 1, 2, 7, 5, 6, 8, 24, 7, 12, 5, 6, 3, 2, 2, 6, 30, 10, 10, 15, 14, 47, 65, 55])
