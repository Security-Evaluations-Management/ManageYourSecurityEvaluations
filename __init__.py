from flask import Flask
from flask_login import LoginManager
from src.models import main_db
import os


def create_app():
    template_dir = os.path.abspath('./myse-frontend/templates')
    static_folder = os.path.abspath('./myse-frontend/static')
    server = Flask(__name__, template_folder=template_dir, static_folder=static_folder)

    server.config['SECRET_KEY'] = os.urandom(12).hex()
    server.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://datfnwhxavwfud' \
                                               ':bc70529444aa8701c3d720e64811509a4b759740149018c2f031b3d00e355a07@ec2' \
                                               '-34-194-171-47.compute-1.amazonaws.com:5432/d4i9o4ipsdq857'
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

    from .src.evidence import evidence_blueprint
    server.register_blueprint(evidence_blueprint)

    from .src.criteria import criteria_blueprint
    server.register_blueprint(criteria_blueprint)

    return server
