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

class Response():

    def send_private_success(self, messages, payload={}):
        private = {}
        private["status"] = "success"
        private["messages"] = messages
        if len(payload) > 0:
            private["payload"] = payload

        return private

    def send_private_failure(self, messages, payload={}):
        private = {}
        private["status"] = "failure"
        private["messages"] = messages
        if len(payload) > 0:
            private["payload"] = payload

        return private

    def send_errors_failure(self, messages, payload={}):
        private = {}
        errors = []
        for input_key, error_list in messages.items():
            for error in error_list:
                errors.append({"type": "error", "message": error})
        private["status"] = "failure"
        private["messages"] = errors

        if len(payload) > 0:
            private["payload"] = payload

        return private

    def send_public_success(self, messages, payload={}):
        public = {}
        public["status"] = "success"
        public["messages"] = messages
        if len(payload) > 0:
            public["payload"] = payload

        return public

    def send_public_failure(self, messages, payload={}):
        public = {}
        public["status"] = "failure"
        public["messages"] = messages
        if len(payload) > 0:
            public["payload"] = payload

        return public

    def send(self, payload={}):
        return payload
