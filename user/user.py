from db import Database
from auth import Auth


class User(object):
    def __init__(self, email: str):
        self._email = email
        self._id = None
        self._password = None
        self.authenticated = 0

    def login(self, password: str):
        #TODO: add AES256 encryption
        self._password = password
        auth = Auth()
        success = auth.login(self._email, self._password)
        if success:
            self.authenticated = 1
            return 1
        else:
            return 0

    def get_id(self):
        return self._email

    def user_id(self):
        return self._id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
