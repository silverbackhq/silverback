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
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.subscriber import Subscriber as SubscriberModule


class Subscribers(View, Controller):
    """Create and List Subscribers Private Endpoint Controller"""

    def __init__(self):
        self.__subscriber = SubscriberModule()

    @allow_if_authenticated
    def post(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "type": "",
            "email": "",
            "phone": "",
            "endpoint": "",
            "auth_token": "",
            "status": ""
        })

        if request_data["type"] == "email":

            self.get_form().add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_email': {
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        elif request_data["type"] == "phone":

            self.get_form().add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'phone': {
                    'value': request_data["phone"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_phone': {
                            'error': _('Error! Phone number is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        else:

            self.get_form().add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_email': {
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'endpoint': {
                    'value': request_data["endpoint"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_url': {
                            'error': _('Error! Endpoint URL is invalid.')
                        }
                    }
                },
                'auth_token': {
                    'value': request_data["auth_token"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'length_between': {
                            'param': [0, 80],
                            'error': _('Error! Token is very long.')
                        },
                        'optional': {}
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        external_id = self.__helpers.generate_uuid()

        while self.__subscriber.get_one_by_external_id(external_id) is not False:
            external_id = self.__helpers.generate_uuid()

        if request_data["type"] == "email":

            result = self.__subscriber.insert_one({
                "status": self.get_form().get_sinput("status"),
                "type": self.get_form().get_sinput("type"),
                "email": self.get_form().get_sinput("email"),
                "phone": "",
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        elif request_data["type"] == "phone":

            result = self.__subscriber.insert_one({
                "status": self.get_form().get_sinput("status"),
                "type": self.get_form().get_sinput("type"),
                "email": "",
                "phone": self.get_form().get_sinput("phone"),
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        else:

            result = self.__subscriber.insert_one({
                "status": self.get_form().get_sinput("status"),
                "type": self.get_form().get_sinput("type"),
                "email": self.get_form().get_sinput("email"),
                "phone": "",
                "endpoint": self.get_form().get_sinput("endpoint"),
                "auth_token": self.get_form().get_sinput("auth_token"),
                "external_id": external_id
            })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Subscriber created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating subscriber.")
            }])

    @allow_if_authenticated
    def get(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("get", {
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
            'subscribers': self.__format_subscribers(self.__subscriber.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__subscriber.count_all()
            }
        })

    def __format_subscribers(self, subscribers):
        subscribers_list = []

        for subscriber in subscribers:
            subscribers_list.append({
                "id": subscriber.id,
                "status": subscriber.status.title(),
                "type": subscriber.type,
                "email": subscriber.email,
                "phone": subscriber.phone,
                "endpoint": subscriber.endpoint,
                "auth_token": subscriber.auth_token,
                "created_at": subscriber.created_at.strftime("%b %d %Y %H:%M:%S"),
                "edit_url": reverse("app.web.admin.subscriber.edit", kwargs={'subscriber_id': subscriber.id}),
                "delete_url": reverse("app.api.private.v1.admin.subscriber.endpoint", kwargs={'subscriber_id': subscriber.id})
            })

        return subscribers_list


class Subscriber(View, Controller):
    """Update and Delete Subscriber Private Endpoint Controller"""

    def __init__(self):
        self.__subscriber = SubscriberModule()

    @allow_if_authenticated
    def post(self, request, subscriber_id):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "type": "",
            "email": "",
            "phone": "",
            "endpoint": "",
            "auth_token": "",
            "status": ""
        })

        if request_data["type"] == "email":

            self.get_form().add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_email': {
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        elif request_data["type"] == "phone":

            self.get_form().add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'phone': {
                    'value': request_data["phone"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_phone': {
                            'error': _('Error! Phone number is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        else:

            self.get_form().add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_email': {
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'endpoint': {
                    'value': request_data["endpoint"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_url': {
                            'error': _('Error! Endpoint URL is invalid.')
                        }
                    }
                },
                'auth_token': {
                    'value': request_data["auth_token"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'length_between': {
                            'param': [0, 80],
                            'error': _('Error! Token is very long.')
                        },
                        'optional': {}
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        if request_data["type"] == "email":

            result = self.__subscriber.update_one_by_id(subscriber_id, {
                "status": self.get_form().get_sinput("status"),
                "type": self.get_form().get_sinput("type"),
                "email": self.get_form().get_sinput("email"),
                "phone": "",
                "endpoint": "",
                "auth_token": ""
            })

        elif request_data["type"] == "phone":

            result = self.__subscriber.update_one_by_id(subscriber_id, {
                "status": self.get_form().get_sinput("status"),
                "type": self.get_form().get_sinput("type"),
                "email": "",
                "phone": self.get_form().get_sinput("phone"),
                "endpoint": "",
                "auth_token": ""
            })

        else:

            result = self.__subscriber.update_one_by_id(subscriber_id, {
                "status": self.get_form().get_sinput("status"),
                "type": self.get_form().get_sinput("type"),
                "email": self.get_form().get_sinput("email"),
                "phone": "",
                "endpoint": self.get_form().get_sinput("endpoint"),
                "auth_token": self.get_form().get_sinput("auth_token")
            })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Subscriber updated successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating subscriber.")
            }])

    @allow_if_authenticated
    def delete(self, request, subscriber_id):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id

        if self.__subscriber.delete_one_by_id(subscriber_id):
            return self.json([{
                "type": "success",
                "message": _("Subscriber deleted successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting subscriber.")
            }])
