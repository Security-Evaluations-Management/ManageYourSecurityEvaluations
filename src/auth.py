from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
# from .models import User
# from .. import user_db
from .Database import *
from .models import User

auth_blueprint = Blueprint('auth', __name__)
db = Database()


@auth_blueprint.route('/login')
def login():
    return render_template('login.html')


@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user_exist = db.check_if_user_exist(email)

    if not user_exist:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    else:
        db_password = db.get_user_hashed_password(email)
        if not check_password_hash(db_password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

    user_info = db.search_user(email)[0]
    user = User(user_info)
    login_user(user, remember=remember)

    return redirect(url_for('main.index'))


@auth_blueprint.route('/signup')
def signup():
    return render_template('signup.html')


@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if db.check_if_user_exist(email):
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    hash_password = generate_password_hash(password, method='sha256', salt_length=16)
    print(hash_password)
    db.add_new_user(name, email, hash_password)
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
