"""
Profile Module
"""

# Django
from django.contrib.auth import update_session_auth_hash

# local Django
from app.modules.util.token import Token
from app.modules.util.helpers import Helpers
from app.modules.util.gravatar import Gravatar
from app.modules.entity.profile_entity import Profile_Entity
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.user_entity import User_Entity


class Profile():

    __option_entity = None
    __user_entity = None
    __helpers = None
    __logger = None
    __token = None
    __profile_entity = None

    def __init__(self):
        self.__option_entity = Option_Entity()
        self.__user_entity = User_Entity()
        self.__helpers = Helpers()
        self.__token = Token()
        self.__profile_entity = Profile_Entity()
        self.__logger = self.__helpers.get_logger(__name__)

    def get_profile(self, user_id):

        profile_data = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "job_title": "",
            "company": "",
            "address": "",
            "github_url": "",
            "twitter_url": "",
            "facebook_url": "",
            "access_token": "",
            "refresh_token": "",
            "avatar": ""
        }

        user = self.__user_entity.get_one_by_id(user_id)
        profile = self.__profile_entity.get_profile_by_user_id(user_id)

        if user is not False:
            profile_data["first_name"] = user.first_name
            profile_data["last_name"] = user.last_name
            profile_data["username"] = user.username
            profile_data["email"] = user.email
            profile_data["avatar"] = Gravatar(user.email).get_image()

        if profile is not False:
            profile_data["job_title"] = profile.job_title
            profile_data["company"] = profile.company
            profile_data["address"] = profile.address
            profile_data["github_url"] = profile.github_url
            profile_data["twitter_url"] = profile.twitter_url
            profile_data["facebook_url"] = profile.facebook_url
            profile_data["access_token"] = profile.access_token
            profile_data["refresh_token"] = profile.refresh_token

        return profile_data

    def update_profile(self, user_id, user_data):
        user_data["user"] = user_id
        if self.__profile_entity.profile_exists(user_data["user"]):
            status = self.__profile_entity.update_profile(user_data)
            status &= self.__user_entity.update_one_by_id(user_data["user"], user_data)
            return status
        else:
            status = (self.__profile_entity.create_profile(user_data) is not False)
            status &= self.__user_entity.update_one_by_id(user_data["user"], user_data)
            return status

    def update_access_token(self, user_id):
        token = self.__token.generate_token()
        while self.__profile_entity.token_used(token) is not False:
            token = self.__token.generate_token()

        return token if self.__profile_entity.update_access_token(user_id, token) else False

    def update_refresh_token(self, user_id):
        token = self.__token.generate_token()
        while self.__profile_entity.token_used(token) is not False:
            token = self.__token.generate_token()

        return token if self.__profile_entity.update_refresh_token(user_id, token) else False

    def get_profile_by_access_token(self, access_token):
        return self.__profile_entity.get_profile_by_access_token(access_token)

    def change_password(self, user_id, password):
        return self.__user_entity.update_password_by_user_id(user_id, password)

    def restore_session(self, user_id, request):
        return update_session_auth_hash(request, self.__user_entity.get_one_by_id(user_id))

    def validate_password(self, user_id, password):
        return self.__user_entity.validate_password_by_user_id(user_id, password)

    def update_user(self, user_id, user_data):
        return self.__user_entity.update_one_by_id(self, user_id, user_data)

    def username_used_elsewhere(self, user_id, username):
        user = self.__user_entity.get_one_by_username(username)
        return False if user is False or user.id == user_id else True

    def email_used_elsewhere(self, user_id, email):
        user = self.__user_entity.get_one_by_email(email)
        return False if user is False or user.id == user_id else True
