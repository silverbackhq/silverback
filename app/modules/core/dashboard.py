"""
Dashboard Module
"""

# Standard Library
import datetime

# Third Party Library
from django.utils import timezone

# Local Library
from app.modules.entity.user_entity import UserEntity
from app.modules.entity.metric_entity import MetricEntity
from app.modules.entity.incident_entity import IncidentEntity
from app.modules.entity.component_entity import ComponentEntity
from app.modules.entity.subscriber_entity import SubscriberEntity
from app.modules.entity.component_group_entity import ComponentGroupEntity
from app.modules.entity.incident_update_entity import IncidentUpdateEntity
from app.modules.entity.incident_update_component_entity import IncidentUpdateComponentEntity
from app.modules.entity.incident_update_notification_entity import IncidentUpdateNotificationEntity


class Dashboard():

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
        self.__incident = IncidentEntity()
        self.__incident_update = IncidentUpdateEntity()
        self.__incident_update_notification = IncidentUpdateNotificationEntity()
        self.__incident_update_component = IncidentUpdateComponentEntity()
        self.__subscriber = SubscriberEntity()
        self.__user = UserEntity()
        self.__component = ComponentEntity()
        self.__component_group = ComponentGroupEntity()
        self.__metric = MetricEntity()

    def incidents_count(self):
        return self.__incident.count_all()

    def subscribers_count(self):
        return self.__subscriber.count_all()

    def components_count(self):
        return self.__component.count_all()

    def component_groups_count(self):
        return self.__component_group.count_all()

    def metrics_count(self):
        return self.__metric.count_all()

    def users_count(self):
        return self.__user.count_all()

    def notifications_count(self, status):
        return self.__incident_update_notification.count_by_status(status)

    def subscribers_chart(self, days=14):
        subscribers = self.__subscriber.count_over_days(days)
        points = self.__build_points(days)
        for subscriber in subscribers:
            key = str(subscriber["day"].strftime("%d-%m-%Y"))
            if key in points.keys():
                points[key] = subscriber["count"]
        return ", ".join(str(x) for x in list(points.values()))

    def components_chart(self, days=14):
        components = self.__incident_update_component.count_over_days(days)
        points = self.__build_points(days)
        for component in components:
            key = str(component["day"].strftime("%d-%m-%Y"))
            if key in points.keys():
                points[key] = component["count"]
        return ", ".join(str(x) for x in list(points.values()))

    def notifications_chart(self, status, days=14):
        notifications = self.__incident_update_notification.count_over_days(status, days)
        points = self.__build_points(days)
        for notification in notifications:
            key = str(notification["day"].strftime("%d-%m-%Y"))
            if key in points.keys():
                points[key] = notification["count"]
        return ", ".join(str(x) for x in list(points.values()))

    def incidents_chart(self, days=14):
        incidents = self.__incident.count_over_days(days)
        points = self.__build_points(days)
        for incident in incidents:
            key = str(incident["day"].strftime("%d-%m-%Y"))
            if key in points.keys():
                points[key] = incident["count"]
        return ", ".join(str(x) for x in list(points.values()))

    def get_open_incidents(self):
        incidents = self.__incident.get_by_status("open")
        incidents_list = []

        for incident in incidents:
            incidents_list.append({
                "id": incident.id,
                "name": incident.name,
                "uri": incident.uri,
                "status": incident.status.title(),
                "created_at": incident.created_at.strftime("%b %d %Y %H:%M:%S")
            })

        return incidents_list

    def get_affected_components(self):
        affected_components = self.__incident_update_component.get_affected_components(0)
        affected_components_list = []

        for affected_component in affected_components:
            affected_components_list.append({
                "id": affected_component.id,
                "name": affected_component.component.name,
                "type": affected_component.type.replace("_", " ").title(),
                "update_id": affected_component.incident_update.id,
                "incident_id": affected_component.incident_update.incident.id
            })

        return affected_components_list

    def __build_points(self, days):
        i = days
        points = {}
        while i >= 0:
            last_x_days = timezone.now() - datetime.timedelta(i)
            points[str(last_x_days.strftime("%d-%m-%Y"))] = 0
            i -= 1
        return points
