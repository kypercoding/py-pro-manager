from flask_login import UserMixin, login_manager
from flask import current_app

from db import user_db as udb


class User(UserMixin):
    def __init__(self, uuid, username, email):
        """
        Initializes user with username
        and password.
        """
        self._uuid = uuid
        self._username = username
        self._email = email
    

    def get_id(self):
        return self._username
    

    def get_uuid(self):
        return self._uuid
