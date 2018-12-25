"""
ACL Module
"""

# Django
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

# local Django
from app.modules.util.helpers import Helpers


class ACL():

    __helpers = None
    __logger = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def new_role(self, name):
        group = Group()
        group.name = name
        group.save()

        return False if group.pk is None else group

    def new_permission(self, name, content_type_id, codename):
        permission = Permission()
        permission.name = name
        permission.content_type_id = content_type_id
        permission.codename = codename
        permission.save()

        return False if permission.pk is None else permission

    def get_role_by_name(self, name):
        try:
            role = Group.objects.get(name=name)
            return False if role.pk is None else role
        except Exception:
            return False

    def get_permission_by_name(self, name):
        try:
            permission = Permission.objects.get(name=name)
            return False if permission.pk is None else permission
        except Exception:
            return False

    def get_permission_by_codename(self, codename):
        try:
            permission = Permission.objects.get(codename=codename)
            return False if permission.pk is None else permission
        except Exception:
            return False

    def get_user_by_id(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return False if user.pk is None else user
        except Exception:
            return False

    def add_permission_to_role(self, permission_codename, role_name):
        role = self.get_role_by_name(role_name)
        permission = self.get_permission_by_codename(permission_codename)

        if role is not False and permission is not False:
            role.permissions.add(permission)
            return True

        return False

    def add_permission_to_user(self, permission_codename, user_id):
        user = self.get_user_by_id(user_id)
        permission = self.get_permission_by_codename(permission_codename)

        if user is not False and permission is not False:
            user.user_permissions.add(permission)
            return True

        return False

    def add_role_to_user(self, role_name, user_id):
        role = self.get_role_by_name(role_name)
        user = self.get_user_by_id(user_id)

        if role is not False and user is not False:
            user.groups.add(role)
            return True

        return False

    def get_content_type(self, label, model):
        try:
            content_type = ContentType.objects.get(app_label=label, model=model)
            return False if content_type.pk is None else content_type
        except Exception:
            return False

    def get_user_content_type(self):
        return ContentType.objects.get_for_model(User)

    def get_content_type_id(self, label, model):
        try:
            content_type = ContentType.objects.get(app_label=label, model=model)
            return False if content_type.pk is None else content_type.id
        except Exception:
            return False

    def truncate_default_permissions(self):
        return Permission.objects.all().delete()

    def get_all_user_permissions(self, user_id):
        user = self.get_user_by_id(user_id)
        if user is not False:
            return user.get_all_permissions()
        return {}

    def get_user_groups_permissions(self, user_id):
        user = self.get_user_by_id(user_id)
        if user is not False:
            return user.get_group_permissions()
        return {}

    def user_has_permission(self, user_id, permission_codename):
        user = self.get_user_by_id(user_id)

        if user is not False:
            return user.has_perm("auth.%s" % permission_codename)

        return False
