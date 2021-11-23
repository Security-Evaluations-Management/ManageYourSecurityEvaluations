from flask_login import UserMixin
from __init__ import user_db


class User(UserMixin, user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key=True)
    password = user_db.Column(user_db.String(100))
    name = user_db.Column(user_db.String(1000))
    email = user_db.Column(user_db.String(100), unique=True)

