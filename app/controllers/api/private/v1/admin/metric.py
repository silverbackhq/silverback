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
from django.views import View
from django.urls import reverse
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.metric import Metric as MetricModule
from app.modules.core.decorators import allow_if_authenticated


class Metrics(View, Controller):
    """Create and List Metrics Private Endpoint Controller"""

    def __init__(self):
        self.__metric = MetricModule()

    @allow_if_authenticated
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "title": "",
            "description": "",
            "source": "",
            "application": "",
            "metric": "",
            "x_axis": "",
            "y_axis": ""
        })

        self.form().add_inputs({
            'title': {
                'value': request_data["title"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 60],
                        'error': _('Error! Metric title must be 1 to 60 characters long.')
                    }
                }
            },
            'description': {
                'value': request_data["description"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 150],
                        'error': _('Error! Metric description must be less than 150 characters long.')
                    },
                    'optional': {}
                }
            },
            'source': {
                'value': request_data["source"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'any_of': {
                        'param': [["newrelic"]],
                        'error': _('Error! Source is invalid.')
                    }
                }
            },
            'application': {
                'value': request_data["application"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 60],
                        'error': _('Error! Application must be 1 to 60 characters long.')
                    }
                }
            },
            'metric': {
                'value': request_data["metric"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 60],
                        'error': _('Error! Metric must be 1 to 60 characters long.')
                    }
                }
            },
            'x_axis': {
                'value': request_data["x_axis"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 40],
                        'error': _('Error! X-Axis label must be 1 to 40 characters long.')
                    }
                }
            },
            'y_axis': {
                'value': request_data["y_axis"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 40],
                        'error': _('Error! Y-Axis label must be 1 to 40 characters long.')
                    }
                }
            }
        })

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        if self.__metric.get_one_by_title(self.form().get_sinput("title")):
            return self.json([{
                "type": "error",
                "message": _("Error! Metric title is used before.")
            }])

        result = self.__metric.insert_one({
            "title": self.form().get_sinput("title"),
            "description": self.form().get_sinput("description"),
            "source": self.form().get_sinput("source"),
            "x_axis": self.form().get_sinput("x_axis"),
            "y_axis": self.form().get_sinput("y_axis"),
            "data": '{"application":"%s", "metric":"%s"}' % (
                self.form().get_sinput("application"),
                self.form().get_sinput("metric")
            )
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Metric created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating metric.")
            }])

    @allow_if_authenticated
    def get(self, request):

        request_data = self.get_request_data(request, "get", {
            "offset": 0,
            "limit": 20
        })

        try:
            offset = int(request_data["offset"])
            limit = int(request_data["limit"])
        except Exception:
            offset = 0
            limit = 20

        return self.json([], {
            'metrics': self.__format_metrics(self.__metric.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__metric.count_all()
            }
        })

    def __format_metrics(self, metrics):
        metrics_list = []

        for metric in metrics:
            metrics_list.append({
                "id": metric.id,
                "title": metric.title,
                "source": metric.source.title(),
                "created_at": metric.created_at.strftime("%b %d %Y %H:%M:%S"),
                "edit_url": reverse("app.web.admin.metric.edit", kwargs={'metric_id': metric.id}),
                "delete_url": reverse("app.api.private.v1.admin.metric.endpoint", kwargs={'metric_id': metric.id})
            })

        return metrics_list


class Metric(View, Controller):
    """Update and Delete Metric Private Endpoint Controller"""

    def __init__(self):
        self.__metric = MetricModule()

    @allow_if_authenticated
    def post(self, request, metric_id):

        request_data = self.get_request_data(request, "post", {
            "title": "",
            "description": "",
            "source": "",
            "application": "",
            "metric": "",
            "x_axis": "",
            "y_axis": ""
        })

        self.form().add_inputs({
            'title': {
                'value': request_data["title"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 60],
                        'error': _('Error! Metric title must be 1 to 60 characters long.')
                    }
                }
            },
            'description': {
                'value': request_data["description"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 150],
                        'error': _('Error! Metric description must be less than 150 characters long.')
                    },
                    'optional': {}
                }
            },
            'source': {
                'value': request_data["source"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'any_of': {
                        'param': [["newrelic"]],
                        'error': _('Error! Source is invalid.')
                    }
                }
            },
            'application': {
                'value': request_data["application"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 60],
                        'error': _('Error! Application must be 1 to 60 characters long.')
                    }
                }
            },
            'metric': {
                'value': request_data["metric"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 60],
                        'error': _('Error! Metric must be 1 to 60 characters long.')
                    }
                }
            },
            'x_axis': {
                'value': request_data["x_axis"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 40],
                        'error': _('Error! X-Axis label must be 1 to 40 characters long.')
                    }
                }
            },
            'y_axis': {
                'value': request_data["y_axis"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 40],
                        'error': _('Error! Y-Axis label must be 1 to 40 characters long.')
                    }
                }
            }
        })

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        current_metric = self.__metric.get_one_by_title(self.form().get_sinput("title"))

        if current_metric and not current_metric["id"] == metric_id:
            return self.json([{
                "type": "error",
                "message": _("Error! Metric title is used before.")
            }])

        result = self.__metric.update_one_by_id(metric_id, {
            "title": self.form().get_sinput("title"),
            "description": self.form().get_sinput("description"),
            "source": self.form().get_sinput("source"),
            "x_axis": self.form().get_sinput("x_axis"),
            "y_axis": self.form().get_sinput("y_axis"),
            "data": '{"application":"%s", "metric":"%s"}' % (
                self.form().get_sinput("application"),
                self.form().get_sinput("metric")
            )
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Metric updated successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating metric.")
            }])

    @allow_if_authenticated
    def delete(self, request, metric_id):

        self.__user_id = request.user.id

        if self.__metric.delete_one_by_id(metric_id):
            return self.json([{
                "type": "success",
                "message": _("Metric deleted successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting metric.")
            }])


class NewRelicApps(View, Controller):
    """List NewRelic Apps Private Endpoint Controller"""

    def __init__(self):
        self.__metric = MetricModule()

    @allow_if_authenticated
    def get(self, request):

        result = False

        try:
            result = self.__metric.get_new_relic_apps()
        except Exception as e:
            self.logger().error(_("Error while listing newrelic applications: %(error)s") % {
                "error": str(e)
            })

        if result is False:
            return self.json([{
                "type": "error",
                "message": _("Error! Connecting to New Relic.")
            }])

        return self.json([], {
            'apps': result
        })
