from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

user_db = SQLAlchemy()


def create_app():
    template_dir = os.path.abspath('./myse-frontend/templates')
    static_folder = os.path.abspath('./myse-frontend/static')
    server = Flask(__name__, template_folder=template_dir, static_folder=static_folder)

    server.config['SECRET_KEY'] = os.urandom(12).hex()
    server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgre:si4848748@localhost:8888/Security Platform'
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    user_db.init_app(server)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(server)

    from .src.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .src.auth import auth_blueprint
    server.register_blueprint(auth_blueprint)

    from .src.main import main_blueprint
    server.register_blueprint(main_blueprint)

    return server