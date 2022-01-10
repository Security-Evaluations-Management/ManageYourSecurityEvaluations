from flask import Flask
from flask_login import LoginManager
from src.models import main_db
import os


def create_app():
    template_dir = os.path.abspath('./myse-frontend/templates')
    static_folder = os.path.abspath('./myse-frontend/static')
    server = Flask(__name__, template_folder=template_dir, static_folder=static_folder)

    server.config['SECRET_KEY'] = os.urandom(12).hex()
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                           'myse-database/main_db.sqlite3')
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(server)

    from .src.models import User
    main_db.init_app(server)
    with server.app_context():
        main_db.create_all()  # create database

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .src.auth import auth_blueprint
    server.register_blueprint(auth_blueprint)

    from .src.main import main_blueprint
    server.register_blueprint(main_blueprint)

    from .src.view import view_blueprint
    server.register_blueprint(view_blueprint)

    from .src.upload import upload_blueprint
    server.register_blueprint(upload_blueprint)

    from .src.search import search_blueprint
    server.register_blueprint(search_blueprint)

    return server
