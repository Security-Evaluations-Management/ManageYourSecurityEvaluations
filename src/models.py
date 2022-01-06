from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

main_db = SQLAlchemy()


class User(main_db.Model, UserMixin):
    id = main_db.Column(main_db.Integer, primary_key=True)
    email = main_db.Column(main_db.String(255, collation='NOCASE'), nullable=False, unique=True)
    password = main_db.Column(main_db.String(255), nullable=False)
    name = main_db.Column(main_db.String(50))
    role_id = main_db.Column(main_db.Integer, main_db.ForeignKey('role.id'), nullable=False)


# Define the Role data-model
class Role(main_db.Model):
    __tablename__ = 'role'
    id = main_db.Column(main_db.Integer(), primary_key=True)
    name = main_db.Column(main_db.String(50), unique=True)
    user = main_db.relationship('User', backref='role', lazy=True)


class Evidence(main_db.Model):
    __tablename__ = 'evidence'
    id = main_db.Column(main_db.Integer, primary_key=True)
    name = main_db.Column(main_db.String(20))

    def __init__(self, name):
        self.name = name


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
