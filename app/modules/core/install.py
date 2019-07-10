"""
Install Module
"""

# Third Party Library
from django.core.management import execute_from_command_line

# Local Library
from app.modules.core.acl import ACL
from app.modules.entity.user_entity import UserEntity
from app.modules.entity.option_entity import OptionEntity


class Install():

    __options = [
        {"key": "app_installed", "value": "true", "autoload": True},
        {"key": "app_description", "value": "", "autoload": False},
        {"key": "google_analytics_account", "value": "", "autoload": True},
        {"key": "reset_mails_messages_count", "value": "5", "autoload": False},
        {"key": "reset_mails_expire_after", "value": "24", "autoload": False},
        {"key": "access_tokens_expire_after", "value": "48", "autoload": False},
        {"key": "prometheus_token", "value": "", "autoload": False},
        {"key": "newrelic_api_key", "value": "", "autoload": False}
    ]
    __admin = {
        "username": "",
        "email": "",
        "password": "",
        "is_superuser": True,
        "is_active": True,
        "is_staff": False
    }
    __option_entity = None
    __user_entity = None
    __acl = None

    def __init__(self):
        self.__option_entity = OptionEntity()
        self.__user_entity = UserEntity()
        self.__acl = ACL()

    def is_installed(self):
        return False if self.__option_entity.get_one_by_key("app_installed") is False else True

    def set_app_data(self, name, email, url):
        self.__options.append({"key": "app_name", "value": name, "autoload": True})
        self.__options.append({"key": "app_email", "value": email, "autoload": True})
        self.__options.append({"key": "app_url", "value": url, "autoload": True})

    def set_admin_data(self, username, email, password):
        self.__admin["username"] = username
        self.__admin["email"] = email
        self.__admin["password"] = password

    def init_base_acl(self, user_id):
        self.__acl.truncate_default_permissions()
        self.__acl.new_role("super_admin")
        self.__acl.new_role("normal_user")
        self.__acl.new_permission("Manage Settings", self.__acl.get_content_type_id("auth", "user"), "manage_settings")
        self.__acl.add_permission_to_role("super_admin", "manage_settings")
        self.__acl.add_role_to_user("super_admin", user_id)
        return True

    def install(self):
        execute_from_command_line(["manage.py", "migrate"])
        status = True
        status &= self.__option_entity.insert_many(self.__options)
        user = self.__user_entity.insert_one(self.__admin)
        status &= (user is not False)

        if user is not False:
            status &= self.init_base_acl(user.id)

        return user.id if status else False

    def uninstall(self):
        self.__option_entity.truncate()
        self.__user_entity.truncate()
