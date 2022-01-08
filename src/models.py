from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

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


def add_evidence(evidence_name):
    if evidence_name:
        evidence = Evidence(evidence_name)
        main_db.session.add(evidence)
        main_db.session.commit()
        return True
    return False


def users_name():
    usernames = [users.name
                 for users in main_db.session.query(User.name).join(Role).filter(Role.name == "DEV")]
    return usernames


def criterias_name():
    criteria_names = [criteria.name
                      for criteria in main_db.session.query(Criteria.name)]
    return criteria_names


def projects_name():
    project_names = [evidence.project_name
                     for evidence in main_db.session.query(Evidence.project_name)]
    return project_names
