"""
Status Page Module
"""

import json
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.incident_entity import Incident_Entity
from app.modules.entity.incident_update_entity import Incident_Update_Entity
from app.modules.entity.incident_update_component_entity import Incident_Update_Component_Entity
from django.utils.translation import gettext as _
from app.modules.entity.component_group_entity import Component_Group_Entity
from app.modules.entity.component_entity import Component_Entity


class Status_Page():

    __option_entity = None
    __incident_entity = None
    __incident_update_entity = None
    __incident_update_component_entity = None
    __component_group_entity = None
    __component_entity = None

    def __init__(self):
        self.__option_entity = Option_Entity()
        self.__incident_entity = Incident_Entity()
        self.__incident_update_entity = Incident_Update_Entity()
        self.__incident_update_component_entity = Incident_Update_Component_Entity()
        self.__component_group_entity = Component_Group_Entity()
        self.__component_entity = Component_Entity()

    def get_system_status(self):
        return "operational"

    def get_about_site(self):
        option = self.__option_entity.get_one_by_key("builder_about")
        return option.value if option else ""

    def get_incident_by_uri(self, uri):
        incident = self.__incident_entity.get_one_by_uri(uri)
        app_name = self.__option_entity.get_one_by_key("app_name")

        if incident:
            incident_data = {
                "headline": incident.name,
                "headline_class": "text-danger",
                "sub_headline": _("Incident Report for %s") % (app_name.value),
                "affected_components": [],
                "updates": []
            }

            updates = self.__incident_update_entity.get_all(incident.id)

            for update in updates:
                incident_data["updates"].append({
                    "type": update.status.title(),
                    "body": update.message,
                    "date": update.datetime
                })

                components = self.__incident_update_component_entity.get_all(update.id)

                for component in components:
                    if component.component.name not in incident_data["affected_components"]:
                        incident_data["affected_components"].append(component.component.name)

            incident_data["affected_components"] = ", ".join(incident_data["affected_components"])

            return incident_data

        return False

    def get_incidents_for_period(self, period):
        return {
            "period": "May 2019 - July 2019",
            "incidents": [
                {
                    "date": "March 2019",
                    "incidents": [
                        {
                            "uri": "123",
                            "subject": "Partial network outage at one of our network suppliers",
                            "class": "text-danger",
                            "final_update": "This incident has been resolved.",
                            "period": "March 7, 08:56 CET - March 8, 2:56 CET"
                        },
                        {
                            "uri": "123",
                            "subject": "Partial network outage at one of our network suppliers",
                            "class": "text-danger",
                            "final_update": "This incident has been resolved.",
                            "period": "March 7, 08:56 CET - March 8, 2:56 CET"
                        },
                    ]
                },
                {
                    "date": "February 2019",
                    "incidents": []
                },
                {
                    "date": "January 2019",
                    "incidents": []
                }
            ]
        }

    def get_past_incidents(self, days):
        return [
            {
                "date": "March 8, 2019",
                "incidents": [
                    {
                        "uri": "123",
                        "subject": "Partial network outage at one of our network suppliers",
                        "class": "text-danger",
                        "updates": [
                            {
                                "type": "Resolved",
                                "date": "March 7, 08:56 CET",
                                "body": "we had a partial network outage at one of our network suppliers."
                            },
                            {
                                "type": "Update",
                                "date": "March 7, 08:56 CET",
                                "body": "we had a partial network outage at one of our network suppliers."
                            },
                        ]
                    },
                    {
                        "uri": "123",
                        "subject": "Partial network outage at one of our network suppliers",
                        "class": "text-danger",
                        "updates": [
                            {
                                "type": "Resolved",
                                "date": "March 7, 08:56 CET",
                                "body": "we had a partial network outage at one of our network suppliers."
                            },
                            {
                                "type": "Update",
                                "date": "March 7, 08:56 CET",
                                "body": "we had a partial network outage at one of our network suppliers."
                            },
                        ]
                    },
                ]
            },
            {
                "date": "March 7, 2019",
                "incidents": []
            },
            {
                "date": "March 6, 2019",
                "incidents": []
            },
            {
                "date": "March 5, 2019",
                "incidents": []
            },
            {
                "date": "March 4, 2019",
                "incidents": []
            },
            {
                "date": "March 3, 2019",
                "incidents": [
                    {
                        "uri": "123",
                        "subject": "Partial network outage at one of our network suppliers",
                        "class": "text-danger",
                        "updates": [
                            {
                                "type": "Resolved",
                                "date": "March 7, 08:56 CET",
                                "body": "we had a partial network outage at one of our network suppliers."
                            },
                            {
                                "type": "Update",
                                "date": "March 7, 08:56 CET",
                                "body": "we had a partial network outage at one of our network suppliers."
                            },
                        ]
                    }
                ]
            }
        ]

    def get_system_metrics(self):

        metrics = [
            {
                "id": "container",
                "title": "Website Dashboard - Average response time",
                "xtitle": "Date",
                "ytitle": "Time (m)",
                "day_data": [
                    {"timestamp": 1554858060000, "value": 0.70},
                    {"timestamp": 1554858120000, "value": 0.80},
                    {"timestamp": 1554858180000, "value": 0.90},
                    {"timestamp": 1554858240000, "value": 0.95}
                ],
                "week_data": [
                    {"timestamp": 1554858060000, "value": 0.75},
                    {"timestamp": 1554858120000, "value": 0.85},
                    {"timestamp": 1554858180000, "value": 0.95},
                    {"timestamp": 1554858240000, "value": 0.98}
                ],
                "month_data": [
                    {"timestamp": 1554858060000, "value": 0.95},
                    {"timestamp": 1554858120000, "value": 0.76},
                    {"timestamp": 1554858180000, "value": 0.43},
                    {"timestamp": 1554858240000, "value": 0.78}
                ],
            }
        ]

        option = self.__option_entity.get_one_by_key("builder_metrics")
        if option:
            items = json.loads(option.value)
            for item in items:
                if "m-" in item:
                    item = item.replace("m-", "")

        return metrics

    def get_services(self):
        services = []
        option = self.__option_entity.get_one_by_key("builder_components")
        if option:
            items = json.loads(option.value)
            for item in items:
                if "c-" in item:
                    component = self.__component_entity.get_one_by_id(item.replace("c-", ""))
                    if component:
                        services.append({
                            "name": component.name,
                            "description": component.description,
                            "current_status": self.get_status(component.id, "component"),
                            "current_status_class": "bg-green",
                            "uptime_chart": self.get_uptime_chart(component.id, "component"),
                            "sub_services": []
                        })
                elif "g-" in item:
                    group = self.__component_group_entity.get_one_by_id(item.replace("g-", ""))
                    services.append({
                        "name": group.name,
                        "description": group.description,
                        "current_status": self.get_status(group.id, "group"),
                        "current_status_class": "bg-green",
                        "uptime_chart": self.get_uptime_chart(group.id, "group"),
                        "sub_services": self.get_sub_services(group.id)
                    })

        return services

    def get_sub_services(self, group_id):
        services = []
        items = self.__component_entity.get_all_components_by_group(group_id)
        for item in items:
            services.append({
                "name": item.name,
                "description": item.description,
                "current_status": self.get_status(item.id, "component"),
                "current_status_class": "bg-green",
                "uptime_chart": self.get_uptime_chart(item.id, "component"),
                "sub_services": []
            })
        return services

    def get_status(self, id, type):
        if type == "component":
            return "Operational"
        elif type == "group":
            return "Operational"

    def get_uptime_chart(self, id, type):
        return []
