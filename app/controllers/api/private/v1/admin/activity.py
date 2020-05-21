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

# Local Library
from app.controllers.controller import Controller
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.activity import Activity as ActivityModule


class Activities(View, Controller):
    """List Activities Private Endpoint Controller"""

    def __init__(self):
        self.__activity = ActivityModule()

    @allow_if_authenticated
    def get(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id
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
            'activities': self.__format_activities(self.__activity.get(self.__user_id, offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__activity.count(self.__user_id)
            }
        })

    def __format_activities(self, activities):
        activities_list = []

        for activity in activities:
            activities_list.append({
                "id": activity.id,
                "activity": activity.activity,
                "created_at": activity.created_at.strftime("%b %d %Y %H:%M:%S")
            })

        return activities_list
