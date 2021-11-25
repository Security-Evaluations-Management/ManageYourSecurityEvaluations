from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import sqlite3
from flask import g

import psycopg2

conn = psycopg2.connect(dbname="Security Platform", user="postgres", password="si4848748", port="8888")

cur = conn.cursor()

user_db = SQLAlchemy()

def create_app():
    server = Flask(__name__)

    server.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:si4848748@localhost:8888/Security Platform"
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    user_db.init_app(server)
    migrate = Migrate(server, user_db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(server)

    from .src.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .src.auth import auth as auth_blueprint
    server.register_blueprint(auth_blueprint)

    from .src.main import main as main_blueprint
    server.register_blueprint(main_blueprint)

    return server
