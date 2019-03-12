"""
Status Page Index Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render

# local Django
from app.modules.core.context import Context
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.decorators import redirect_if_not_installed


class Status_Page_Index(View):

    template_name = 'templates/status_page_index.html'
    __context = None
    __option_entity = None

    @redirect_if_not_installed
    def get(self, request):

        self.__context = Context()
        self.__option_entity = Option_Entity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated,
            "system_status": "operational",
            "about_site": "",
            "past_incidents": [
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
            ],
            "system_metrics": [
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
        })

        return render(request, self.template_name, self.__context.get())


class Status_Page_History(View):

    template_name = 'templates/status_page_history.html'
    __context = None
    __option_entity = None

    @redirect_if_not_installed
    def get(self, request):

        self.__context = Context()
        self.__option_entity = Option_Entity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated,
            "system_status": "operational",
            "about_site": "",
            "prev_link": "#prev",
            "next_link": "#next",
            "history_period": "May 2019 - July 2019",
            "past_incidents": [
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
            ],
        })

        return render(request, self.template_name, self.__context.get())


class Status_Page_Single(View):

    template_name = 'templates/status_page_single.html'
    __context = None
    __option_entity = None

    @redirect_if_not_installed
    def get(self, request, uri):

        self.__context = Context()
        self.__option_entity = Option_Entity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated,
            "uri": uri,
            "system_status": "operational"
        })

        return render(request, self.template_name, self.__context.get())
