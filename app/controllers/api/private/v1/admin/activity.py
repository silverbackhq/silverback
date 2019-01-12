"""
User API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.activity import Activity as Activity_Module


class Activities(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __activity = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__activity = Activity_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def get(self, request):

        self.__user_id = request.user.id

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("get", {
            "offset": "",
            "limit": ""
        })

        try:
            offset = int(request_data["offset"])
            limit = int(request_data["limit"])
        except Exception:
            offset = 0
            limit = 0

        return JsonResponse(self.__response.send_private_success([], {
            'activities': self.__format_activities(self.__activity.get(self.__user_id, offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__activity.count(self.__user_id)
            }
        }))

    def __format_activities(self, activities):
        activities_list = []

        for activity in activities:
            activities_list.append({
                "id": activity.id,
                "activity": activity.activity,
                "created_at": activity.created_at.strftime("%b %d %Y %H:%M:%S")
            })

        return activities_list