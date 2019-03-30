"""
Builder API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from pyvalitron.form import Form
from app.modules.validation.extension import ExtraRules
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.settings import Settings


class Builder_System_Metrics(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):
        pass

    def delete(self, request, metric_id):
        pass


class Builder_Components(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):
        pass

    def delete(self, request, component_id):
        pass


class Builder_Settings(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __settings = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__settings = Settings()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "builder_headline": "",
            "builder_fav_icon_url": "",
            "builder_cover_image_url": "",
            "builder_about": ""
        })

        self.__form.add_inputs({
            'builder_headline': {
                'value': request_data["builder_headline"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 100],
                        'error': _('Error! Headline is very long.')
                    },
                    'optional': {}
                }
            },
            'builder_fav_icon_url': {
                'value': request_data["builder_fav_icon_url"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Favicon url is invalid.')
                    }
                }
            },
            'builder_cover_image_url': {
                'value': request_data["builder_cover_image_url"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Image url is invalid.')
                    }
                }
            },
            'builder_about': {
                'value': request_data["builder_about"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 20000],
                        'error': _('Error! About is very long.')
                    },
                    'optional': {}
                }
            },
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors()))

        result = self.__settings.update_options({
            "builder_headline": self.__form.get_sinput("builder_headline"),
            "builder_fav_icon_url": self.__form.get_sinput("builder_fav_icon_url"),
            "builder_cover_image_url": self.__form.get_sinput("builder_cover_image_url"),
            "builder_about": self.__form.get_sinput("builder_about")
        })

        if result:

            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Builder Settings updated successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating settings.")
            }]))
