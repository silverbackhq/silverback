"""
User API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.urls import reverse

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.user import User as User_Module


class Users(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __user_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__user_module = User_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request):
        pass

    def get(self, request):

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
            'users': self.__format_users(self.__user_module.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__user_module.count_all() + 2
            }
        }))

    def __format_users(self, users):
        users_list = []

        for user in users:
            users_list.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": "Admin" if user.is_superuser == 1 else "User",
                "created_at": user.date_joined.strftime("%b %d %Y %H:%M:%S"),
                "edit_url": reverse("app.web.admin.user.edit", kwargs={'user_id': user.id}),
                "delete_url": reverse("app.api.private.v1.admin.user.endpoint", kwargs={'user_id': user.id})
            })

        return users_list


class User(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __user_module = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__user_module = User_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def put(self, request, user_id):
        pass

    def delete(self, request, user_id):

        self.__user_id = request.user.id

        if self.__user_module.delete_one_by_id(user_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("User deleted successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting a user.")
            }]))
