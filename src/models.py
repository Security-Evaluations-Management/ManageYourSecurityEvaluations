from flask_login import UserMixin
from __init__ import user_db


class User:

    def __init__(self, user_info):
        self.id = user_info[0]
        self.name = user_info[1]
        self.email = user_info[2]
        self.password = user_info[3]