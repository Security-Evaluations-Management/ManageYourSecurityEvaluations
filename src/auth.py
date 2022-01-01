from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required
# from .models import User
# from .. import user_db
from .Database import *

auth_blueprint = Blueprint('auth', __name__)
db = Database()


@auth_blueprint.route('/login')
def login():
    if 'loggedin' in session:
        return redirect(url_for('auth.profile'))
    return render_template('login.html')


@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

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
        session['loggedin'] = True
        session['id'] = user_info[0]
        session['username'] = user_info[1]
        session['email'] = user_info[2]

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
    db.add_new_developer(name, email, hash_password)
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('main.index'))


@auth_blueprint.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html', id=session['id'], username=session['username'], email=session['email'])
    return redirect(url_for('auth.login'))
