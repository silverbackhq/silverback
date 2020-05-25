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

# Standard Library
import json

# Third Party Library
from django.views import View
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.settings import Settings
from app.modules.core.metric import Metric as MetricModule
from app.modules.core.component import Component as ComponentModule
from app.modules.core.decorators import allow_if_authenticated_and_has_permission
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule


class BuilderSystemMetrics(View, Controller):
    """Add and Remove Builder System Metrics Private Endpoint Controller"""

    def __init__(self):
        self.__settings = Settings()
        self.__metric = MetricModule()

    @allow_if_authenticated_and_has_permission("manage_settings")
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "metric_id": ""
        })

        if request_data["metric_id"] == "" or not self.__metric.get_one_by_id(request_data["metric_id"].replace("m-", "")):
            return self.json([{
                "type": "error",
                "message": _("Error! Metric is required.")
            }])

        metrics = self.__settings.get_value_by_key(
            "builder_metrics",
            json.dumps([])
        )

        metrics = json.loads(metrics)

        if request_data["metric_id"] in metrics:
            return self.json([{
                "type": "success",
                "message": _("Metric added successfully.")
            }])

        metrics.append(request_data["metric_id"])

        result = self.__settings.update_options({
            "builder_metrics": json.dumps(metrics)
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Metric added successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while adding metric.")
            }])

    @allow_if_authenticated_and_has_permission("manage_settings")
    def delete(self, request, metric_id):

        metrics = self.__settings.get_value_by_key(
            "builder_metrics",
            json.dumps([])
        )

        metrics = json.loads(metrics)

        if metric_id not in metrics:
            return self.json([{
                "type": "success",
                "message": _("Metric deleted successfully.")
            }])

        metrics.remove(metric_id)

        result = self.__settings.update_options({
            "builder_metrics": json.dumps(metrics)
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Metric deleted successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting metric.")
            }])


class BuilderComponents(View, Controller):
    """Add and Remove Builder Components Private Endpoint Controller"""

    def __init__(self):
        self.__settings = Settings()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()

    @allow_if_authenticated_and_has_permission("manage_settings")
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "component_id": ""
        })

        if request_data["component_id"] == "" or ("c-" not in request_data["component_id"] and "g-" not in request_data["component_id"]):
            return self.json([{
                "type": "error",
                "message": _("Error! Compnent or compnent group is required.")
            }])

        if "c-" in request_data["component_id"] and not self.__component.get_one_by_id(request_data["component_id"].replace("c-", "")):
            return self.json([{
                "type": "error",
                "message": _("Error! Compnent or compnent group is required.")
            }])

        if "g-" in request_data["component_id"] and not self.__component_group.get_one_by_id(request_data["component_id"].replace("g-", "")):
            return self.json([{
                "type": "error",
                "message": _("Error! Compnent or compnent group is required.")
            }])

        components = self.__settings.get_value_by_key(
            "builder_components",
            json.dumps([])
        )

        components = json.loads(components)

        if request_data["component_id"] in components:
            return self.json([{
                "type": "success",
                "message": _("Component added successfully.")
            }])

        components.append(request_data["component_id"])

        result = self.__settings.update_options({
            "builder_components": json.dumps(components)
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Component added successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while adding component.")
            }])

    @allow_if_authenticated_and_has_permission("manage_settings")
    def delete(self, request, component_id):

        components = self.__settings.get_value_by_key(
            "builder_components",
            json.dumps([])
        )

        components = json.loads(components)

        if component_id not in components:
            return self.json([{
                "type": "success",
                "message": _("Component deleted successfully.")
            }])

        components.remove(component_id)

        result = self.__settings.update_options({
            "builder_components": json.dumps(components)
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Component deleted successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting component.")
            }])


class BuilderSettings(View, Controller):
    """Update Builder Settings Private Endpoint Controller"""

    def __init__(self):
        self.__settings = Settings()

    @allow_if_authenticated_and_has_permission("manage_settings")
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "builder_headline": "",
            "builder_favicon_url": "",
            "builder_logo_url": "",
            "builder_about": ""
        })

        self.form().add_inputs({
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
            'builder_favicon_url': {
                'value': request_data["builder_favicon_url"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Favicon URL is invalid.')
                    }
                }
            },
            'builder_logo_url': {
                'value': request_data["builder_logo_url"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Logo URL is invalid.')
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

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        result = self.__settings.update_options({
            "builder_headline": self.form().get_sinput("builder_headline"),
            "builder_favicon_url": self.form().get_sinput("builder_favicon_url"),
            "builder_logo_url": self.form().get_sinput("builder_logo_url"),
            "builder_about": self.form().get_sinput("builder_about")
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Settings updated successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating settings.")
            }])
