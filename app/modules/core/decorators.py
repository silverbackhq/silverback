# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Third Party Library
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.http import Http404

# Local Library
from app.modules.core.acl import ACL
from app.modules.util.helpers import Helpers
from app.modules.entity.option_entity import OptionEntity


def allow_if_authenticated_and_has_permission(permission):
    def wrapper(function):
        def wrap(controller, request, *args, **kwargs):
            acl = ACL()
            if not request.user or not request.user.is_authenticated or not acl.user_has_permission(request.user.id, permission):
                return JsonResponse({
                    "status": "failure",
                    "messages": [{
                        "type": "error",
                        "message": _("Oops! Access forbidden.")
                    }]
                })
            return function(controller, request, *args, **kwargs)
        return wrap
    return wrapper


def redirect_if_not_has_permission(permission):
    def wrapper(function):
        def wrap(controller, request, *args, **kwargs):
            acl = ACL()
            if not request.user or not request.user.is_authenticated or not acl.user_has_permission(request.user.id, permission):
                raise Http404("Page not found.")
            return function(controller, request, *args, **kwargs)
        return wrap
    return wrapper


def redirect_if_authenticated(function):
    def wrap(controller, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            if "redirect" in request.GET:
                return redirect(request.GET["redirect"])
            return redirect("app.web.admin.dashboard")
        return function(controller, request, *args, **kwargs)
    return wrap


def login_if_not_authenticated_or_no_permission(permission):
    def wrapper(function):
        def wrap(controller, request, *args, **kwargs):
            acl = ACL()
            if not request.user or not request.user.is_authenticated:
                return redirect(reverse("app.web.login") + "?redirect=" + request.get_full_path())
            if permission and not acl.user_has_permission(request.user.id, permission):
                raise Http404("Page not found.")
            return function(controller, request, *args, **kwargs)
        return wrap
    return wrapper


def login_if_not_authenticated(function):
    def wrap(controller, request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return redirect(reverse("app.web.login") + "?redirect=" + request.get_full_path())
        return function(controller, request, *args, **kwargs)
    return wrap


def stop_request_if_authenticated(function):
    def wrap(controller, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return JsonResponse({
                "status": "failure",
                "messages": [{
                    "type": "error",
                    "message": _("Error! Access forbidden for authenticated users.")
                }]
            })
        return function(controller, request, *args, **kwargs)
    return wrap


def allow_if_authenticated(function):
    def wrap(controller, request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return JsonResponse({
                "status": "failure",
                "messages": [{
                    "type": "error",
                    "message": _("Oops! Access forbidden.")
                }]
            })
        return function(controller, request, *args, **kwargs)
    return wrap


def redirect_if_not_installed(function):
    def wrap(controller, request, *args, **kwargs):
        installed = False if OptionEntity().get_one_by_key("app_installed") is False else True
        if not installed:
            return redirect("app.web.install")
        return function(controller, request, *args, **kwargs)
    return wrap


def protect_metric_with_auth_key(function):
    def wrap(controller, request, *args, **kwargs):
        if kwargs["type"] == "prometheus":
            prometheus_token = OptionEntity().get_one_by_key("prometheus_token")
            if prometheus_token.value != "" and ("HTTP_AUTHORIZATION" not in request.META or prometheus_token.value != request.META["HTTP_AUTHORIZATION"]):
                raise Http404("Host not found.")
        return function(controller, request, *args, **kwargs)
    return wrap


def stop_request_if_installed(function):
    def wrap(controller, request, *args, **kwargs):
        installed = False if OptionEntity().get_one_by_key("app_installed") is False else True
        if installed:
            return JsonResponse({
                "status": "failure",
                "messages": [{
                    "type": "error",
                    "message": _("Error! Application is already installed.")
                }]
            })
        return function(controller, request, *args, **kwargs)
    return wrap


def log_request_data(function):
    def wrap(controller, request, *args, **kwargs):
        correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        helper = Helpers()
        logger = helper.get_logger(__name__)
        logger.debug(_("Request Method: %(method)s {'correlationId':'%(correlationId)s'}") % {
            "method": request.method,
            "correlationId": correlation_id
        })
        logger.debug(_("Request URL: %(path)s {'correlationId':'%(correlationId)s'}") % {
            "path": request.path,
            "correlationId": correlation_id
        })
        logger.debug(_("Request Body: %(body)s {'correlationId':'%(correlationId)s'}") % {
            "body": request.body,
            "correlationId": correlation_id
        })
        return function(controller, request, *args, **kwargs)
    return wrap
