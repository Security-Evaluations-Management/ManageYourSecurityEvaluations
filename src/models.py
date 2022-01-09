from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

main_db = SQLAlchemy()


class User(main_db.Model, UserMixin):
    id = main_db.Column(main_db.Integer, primary_key=True)
    name = main_db.Column(main_db.String(50))
    email = main_db.Column(main_db.String(120, collation='NOCASE'), nullable=False, unique=True)
    password = main_db.Column(main_db.String(88), nullable=False)
    role_id = main_db.Column(main_db.Integer, main_db.ForeignKey('role.id'), nullable=False)
    criteria = main_db.relationship('Criteria', backref='user', lazy='dynamic')
    evidence = main_db.relationship('Evidence', backref='user', lazy='dynamic')


# Define the Role data-model
class Role(main_db.Model):
    __tablename__ = 'role'
    id = main_db.Column(main_db.Integer(), primary_key=True)
    name = main_db.Column(main_db.String(50), unique=True)
    user = main_db.relationship('User', backref='role', lazy='dynamic')


class Evidence(main_db.Model):
    __tablename__ = 'evidence'
    id = main_db.Column(main_db.Integer, primary_key=True)
    name = main_db.Column(main_db.String(20))
    project_name = main_db.Column(main_db.String(20), nullable=False)
    create_date_time = main_db.Column(main_db.DateTime, nullable=False)
    last_edit_time = main_db.Column(main_db.DateTime, nullable=False)
    description = main_db.Column(main_db.String(200))
    url = main_db.Column(main_db.String(2048), nullable=False)
    user_id = main_db.Column(main_db.Integer, main_db.ForeignKey('user.id'), nullable=False)
    criteria_id = main_db.Column(main_db.Integer, main_db.ForeignKey('criteria.id'), nullable=False)

    def __init__(self, name, project_name, description, url, user_id, criteria_id):
        self.name = name
        self.project_name = project_name
        self.create_date_time = datetime.now()
        self.last_edit_time = datetime.now()
        self.description = description
        self.url = url
        self.user_id = user_id
        self.criteria_id = criteria_id


class Criteria(main_db.Model):
    __tablename__ = 'criteria'
    id = main_db.Column(main_db.Integer, primary_key=True)
    name = main_db.Column(main_db.String(20))
    description = main_db.Column(main_db.String(200))
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


def add_evidence(evidence_name, project_name, description, url, user_id, criteria_id):
    if evidence_name and project_name and url and user_id and criteria_id:
        evidence = Evidence(evidence_name, project_name, description, url, user_id, criteria_id)
        main_db.session.add(evidence)
        main_db.session.commit()
        return True
    return False


# get all developers' name as a list
def users_name():
    usernames = [users.name
                 for users in main_db.session.query(User.name).join(Role).filter(Role.name == "DEV")]
    usernames = list(dict.fromkeys(usernames))
    return usernames


# get all criteria name as a list
def criterias_name():
    criteria_names = [criteria.name
                      for criteria in main_db.session.query(Criteria.name)]
    criteria_names = list(dict.fromkeys(criteria_names))
    return criteria_names


# get all project name as a list
def projects_name():
    project_names = [evidence.project_name
                     for evidence in main_db.session.query(Evidence.project_name)]
    project_names = list(dict.fromkeys(project_names))
    return project_names


# get evidence as a dictionary through evidence id
def get_evidence_info(evidence_id):
    evidence = Evidence.query.filter_by(id=evidence_id).first().__dict__
    evidence.pop('_sa_instance_state', None)
    return evidence


# get evidence by filters
def get_info_by_filter(criteria_name, project_name, employee_name, create_time, last_edit_time, evidence_id):
    if all(v is None for v in [criteria_name, project_name, employee_name, create_time, last_edit_time, evidence_id]):
        return None
    else:
        sql = "select " \
              "evidence.id, evidence.name, project_name, create_date_time, last_edit_time, evidence.description, url " \
              "from evidence join user on evidence.user_id = user.id" \
              " join criteria on evidence.criteria_id = criteria.id where"
        if criteria_name:
            sql += (" criteria.name=\"" + criteria_name + "\"")
        if project_name:
            if any(v is not None for v in [criteria_name]):
                sql += " and"
            sql += (" project_name=\"" + project_name + "\"")
        if employee_name:
            if any(v is not None for v in [criteria_name, project_name]):
                sql += " and"
            sql += (" user.name=\"" + employee_name + "\"")
        if create_time:
            create_time = convert_date_format(create_time)
            if any(v is not None for v in [criteria_name, project_name, employee_name]):
                sql += " and"
            sql += (" create_date_time between date(\"" + create_time + "\")" + " and " + "date(\"" + add_one_day(create_time) + "\")")
        if last_edit_time:
            last_edit_time = convert_date_format(last_edit_time)
            if any(v is not None for v in [criteria_name, project_name, employee_name, create_time]):
                sql += " and"
            sql += (" last_edit_time between date(\"" + last_edit_time + "\")" + " and " + "date(\"" + add_one_day(last_edit_time) + "\")")
        if evidence_id:
            if any(v is not None for v in [criteria_name, project_name, employee_name, create_time, last_edit_time]):
                sql += " and"
            sql += (" evidence.id=" + evidence_id)
        result = main_db.engine.execute(sql)
        return result.fetchall()


# convert date format from yyyy/mm/dd to yyyy-mm-dd
def convert_date_format(date):
    return datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")


# add one more day for given date string, which format is yyyy-mm-dd
def add_one_day(date):
    return (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
