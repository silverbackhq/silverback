"""
Login Module
"""

# Django
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.user_entity import User_Entity


class Login():

    __option_entity = None
    __user_entity = None
    __helpers = None
    __logger = None

    def __init__(self):
        self.__option_entity = Option_Entity()
        self.__user_entity = User_Entity()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def is_authenticated(self, request):
        if request.user and request.user.is_authenticated:
            return True
        else:
            return False

    def authenticate(self, username_email, password, request=None, with_login=True):
        is_email = False
        try:
            is_email = True if validate_email(username_email) is None else False
        except Exception:
            is_email = False
        if is_email:
            user = self.__user_entity.get_one_by_email(username_email)
            if user is not False and user.check_password(password) is True:
                if with_login:
                    self.login(request, user)
                return True
            else:
                return False
        else:
            user = authenticate(request=request, username=username_email, password=password)
            if user is not None:
                if with_login:
                    self.login(request, user)
                return True
            else:
                return False

    def login(self, request, user):
        return login(request, user)
