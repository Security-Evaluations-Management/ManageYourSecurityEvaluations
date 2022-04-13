from flask import Flask
from flask_login import LoginManager
from flask_login import UserMixin
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update, and_, Table

import os

from sqlalchemy import update

template_dir = os.path.abspath('Platform/frontend/templates')
static_folder = os.path.abspath('Platform/frontend/static')
server = Flask(__name__, template_folder=template_dir, static_folder=static_folder)

server.config['SECRET_KEY'] = os.urandom(12).hex()
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://empkuwsyisdhch:a9cf00df71d95ca68a69b120' \
                                          '6664c0fb801ef4eab6ecf443f1de5e0bd6876b80@ec2-44-194-167-63.' \
                                          'compute-1.amazonaws.com:5432/deuoe3ubmqjkhn'
# server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
#                                                                      'main_db.sqlite3')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SECRET_KEY'] = os.urandom(24)

main_db = SQLAlchemy(server)


def create_app():
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(server)

    with server.app_context():
        main_db.create_all()  # create database

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from Platform.src.auth import auth_blueprint
    server.register_blueprint(auth_blueprint)

    from Platform.src.main import main_blueprint
    server.register_blueprint(main_blueprint)

    from Platform.src.evidence import evidence_blueprint
    server.register_blueprint(evidence_blueprint)

    from Platform.src.criteria import criteria_blueprint
    server.register_blueprint(criteria_blueprint)

    return server


class User(main_db.Model, UserMixin):
    id = main_db.Column(main_db.Integer, primary_key=True)
    name = main_db.Column(main_db.String)
    email = main_db.Column(main_db.String, nullable=False, unique=True)
    password = main_db.Column(main_db.String(128), nullable=False)
    role_id = main_db.Column(main_db.Integer, main_db.ForeignKey('role.id'), nullable=False)
    criteria = main_db.relationship('Criteria', backref='user', lazy='dynamic')
    evidence = main_db.relationship('Evidence', backref='user', lazy='dynamic')


# Define the Role data-model
class Role(main_db.Model):
    __tablename__ = 'role'
    id = main_db.Column(main_db.Integer(), primary_key=True)
    name = main_db.Column(main_db.String, unique=True)
    user = main_db.relationship('User', backref='role', lazy='dynamic')


class Evidence(main_db.Model):
    __tablename__ = 'evidence'
    id = main_db.Column(main_db.Integer, primary_key=True)
    name = main_db.Column(main_db.String, unique=True)
    project_name = main_db.Column(main_db.String, nullable=False)
    create_date_time = main_db.Column(main_db.DateTime, nullable=False)
    last_edit_time = main_db.Column(main_db.DateTime, nullable=False)
    description = main_db.Column(main_db.String)
    content = main_db.Column(main_db.String, nullable=False)
    status = main_db.Column(main_db.Integer)
    user_id = main_db.Column(main_db.Integer, main_db.ForeignKey('user.id'), nullable=False)
    criteria_id = main_db.Column(main_db.Integer, main_db.ForeignKey('criteria.id'), nullable=False)

    def __init__(self, name, project_name, description, content, user_id, criteria_id):
        self.name = name
        self.project_name = project_name
        self.create_date_time = datetime.now().replace(microsecond=0)
        self.last_edit_time = datetime.now().replace(microsecond=0)
        self.description = description
        self.content = content
        self.status = 0
        self.user_id = user_id
        self.criteria_id = criteria_id


class Criteria(main_db.Model):
    __tablename__ = 'criteria'
    id = main_db.Column(main_db.Integer, primary_key=True)
    name = main_db.Column(main_db.String, unique=True)
    description = main_db.Column(main_db.String)
    user_id = main_db.Column(main_db.Integer, main_db.ForeignKey('user.id'), nullable=False)
    evidence = main_db.relationship('Evidence', backref='criteria', lazy='dynamic')


def add_new_user(email, password, name):
    new_user = User(email=email, password=password, name=name)

    if User.query.count() == 0:  # no user exist
        default_role = 'Admin'
    else:
        default_role = 'User'
    user_role = Role.query.filter_by(name=default_role).first()
    if not user_role:
        user_role = Role(name=default_role)

    user_role.user.append(new_user)
    main_db.session.add(new_user)
    main_db.session.commit()
    return True


def update_user(user_id, name, role):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return False

    new_role = Role.query.filter_by(name=role).first()
    if not new_role:
        new_role = Role(name=role)

    user.name = name
    new_role.user.append(user)
    main_db.session.commit()
    return True


def update_user_name(user_id, new_name):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return False
    user.name = new_name
    main_db.session.commit()
    return True


def update_user_password(user_id, new_password):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return False
    user.password = new_password
    main_db.session.commit()
    return True


def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    main_db.session.commit()
    return True


def user_exist(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return True
    return False


def get_user(email):
    user = User.query.filter_by(email=email).first()
    return user


def get_all_users():
    users = User.query.all()
    return users


def get_all_criteria():
    return Criteria.query.all()


def add_criteria(name, description, creator):
    new_criteria = Criteria(name=name, description=description)

    creator = User.query.filter_by(name=creator.name).first()
    if not creator:
        return False

    creator.criteria.append(new_criteria)
    main_db.session.add(new_criteria)
    main_db.session.commit()
    return True


def remove_criteria(criteria_id):
    Criteria.query.filter_by(id=criteria_id).delete()
    main_db.session.commit()
    return True


def add_evidence(evidence_name, project_name, description, content, user_id, criteria_id):
    if evidence_name and project_name and content and user_id and criteria_id:
        evidence = Evidence(evidence_name, project_name, description, content, user_id, criteria_id)
        main_db.session.add(evidence)
        main_db.session.commit()
        return Evidence.query.filter_by(name=evidence_name).first().id
    return False


# get all developers' name as a list
def users_name():
    usernames = [users.name
                 for users in main_db.session.query(User.name).join(Role).filter(Role.name == "DEV")]
    usernames = list(dict.fromkeys(usernames))
    return usernames


# get all criteria name as a list
def get_all_criteria_name():
    criteria_names = [criteria.name
                      for criteria in main_db.session.query(Criteria.name)]
    criteria_names = list(dict.fromkeys(criteria_names))
    return criteria_names


def get_all_failed_evidence(user_id):
    evidence = main_db.session.query(Evidence).join(User).filter(User.id == user_id, Evidence.status == -1).all()
    return evidence

# get a pair of criteria id and name
def criteria_id_name():
    sql = "select id, name from criteria"
    result = main_db.engine.execute(sql)
    return result.fetchall()


# get all project name as a list
def projects_name():
    project_names = [evidence.project_name
                     for evidence in main_db.session.query(Evidence.project_name)]
    project_names = list(dict.fromkeys(project_names))
    return project_names


# get evidence as a dictionary through evidence idF
def get_evidence_info(evidence_id):
    evidence = Evidence.query.filter_by(id=evidence_id).first().__dict__
    evidence.pop('_sa_instance_state', None)
    return evidence


def no_filter_search_result():
    sql = "select " \
          "evidence.id, evidence.name, project_name, create_date_time, last_edit_time, evidence.description, content " \
          "from evidence join user on evidence.user_id = user.id" \
          " join criteria on evidence.criteria_id = criteria.id"
    result = main_db.engine.execute(sql)
    return result.fetchall()


# get evidence by filters
def get_info_by_filter(criteria_name, project_name, employee_name, create_time, last_edit_time, evidence_id):
    evidence = main_db.session.query(Evidence.id, Evidence.name, Evidence.project_name, Evidence.create_date_time,
                                     Evidence.last_edit_time, Evidence.status).join(Criteria).join(User)
    if all(v is None for v in [criteria_name, project_name, employee_name, create_time, last_edit_time, evidence_id]):
        return evidence
    else:
        if criteria_name:
            evidence = evidence.filter(Criteria.name == criteria_name)
        if project_name:
            evidence = evidence.filter(Evidence.project_name == project_name)
        if employee_name:
            evidence = evidence.filter(User.name == employee_name)
        if create_time:
            create_time = convert_date_format(create_time)
            evidence = evidence.filter(
                and_(Evidence.create_date_time > create_time, Evidence.create_date_time < add_one_day(create_time)))
        if last_edit_time:
            last_edit_time = convert_date_format(last_edit_time)
            evidence = evidence.filter(
                and_(Evidence.last_edit_time > last_edit_time, Evidence.last_edit_time < add_one_day(last_edit_time)))
        if evidence_id:
            evidence = evidence.filter(Evidence.id == evidence_id)
        return evidence


# get evidence info in detail through evidence id
def get_evidence_by_id(evidence_id):
    sql = "select " \
          "evidence.id, evidence.name, project_name, create_date_time, last_edit_time, evidence.description, content, "\
          "criteria.id, criteria.name, criteria.description " \
          "from evidence join user on evidence.user_id = user.id" \
          " join criteria on evidence.criteria_id = criteria.id where evidence.id =" + evidence_id
    result = main_db.engine.execute(sql)
    return result.fetchall()


# update evidence description
def update_evidence_des(evidence_id, new_description):
    evidence = Evidence.query.filter_by(id=evidence_id).first()
    if not evidence:
        return False
    evidence.description = new_description
    evidence.last_edit_time = datetime.now().replace(microsecond=0)
    main_db.session.commit()
    return True


# update evidence content
def update_evidence_with_file(evidence_id, new_description, contents):
    evidence = Evidence.query.filter_by(id=evidence_id).first()
    if not evidence:
        return False
    evidence.description = new_description
    evidence.last_edit_time = datetime.now().replace(microsecond=0)
    evidence.content = contents
    main_db.session.commit()
    return True


# convert date format from yyyy/mm/dd to yyyy-mm-dd
def convert_date_format(date):
    return datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")


# add one more day for given date string, which format is yyyy-mm-dd
def add_one_day(date):
    return (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')


def get_criteria_by_id(criteria_id):
    criteria = Criteria.query.filter_by(id=criteria_id).first()
    return criteria


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def get_evidence_by_userid(user_id):
    evidence = main_db.session.query(Evidence).join(User).filter(User.id == user_id).all()
    return evidence


def delete_evidence(evidence_id):
    result = Evidence.query.filter_by(id=evidence_id).first()
    print(result)
    if result is not None:
        Evidence.query.filter_by(id=evidence_id).delete()
        main_db.session.commit()
        return True
    else:
        return False


# get the evidence status according to the id
def get_evidence_status(evidence_id):
    result = main_db.session.query(Evidence.status).filter(Evidence.id == evidence_id)
    return result


# update new evidence status according to the id
def update_evidence_status(evidence_id, new_status):
    stmt = update(Evidence).where(Evidence.id == evidence_id).values(status=new_status)
    main_db.engine.execute(stmt)
