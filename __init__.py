from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

user_db = SQLAlchemy()


def create_app():
    server = Flask(__name__)

    server.config['SECRET_KEY'] = os.urandom(12).hex()
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                           'database/user_db.sqlite3')
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    user_db.init_app(server)

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