import re

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from Platform import *
from Platform.src.include.access_controller import approve_access

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login')
def login():
    return render_template('login.html')


@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    entered_password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if user_exist(email):
        user = get_user(email)
        if check_password_hash(user.password, entered_password):
            login_user(user, remember=remember)
            return redirect(url_for('main.home'))

    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/signup')
def signup():
    return render_template('signup.html')


@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    strong_password = check_password(password)

    if user_exist(email):
        flash('Email address already exists. Please login!')
        return redirect(url_for('auth.signup'))
    elif not strong_password:
        flash('Please follow the password rules.')
        return redirect(url_for('auth.signup'))

    add_new_user(email, generate_password_hash(password, method='sha256', salt_length=32), name)

    return redirect(url_for('auth.login'))


def check_password(password):
    strong_password = not (len(password) < 8 or re.search(r"\d", password) is None
                           or re.search(r"[A-Z]", password) is None or re.search(r"[a-z]", password) is None)
    return strong_password


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@auth_blueprint.route('/admin')
@login_required
def admin():
    if not approve_access(current_user.role.name, 'admin'):
        abort(403)

    user_list = get_all_users()
    return render_template('admin.html', user_list=user_list, current_user=current_user)


@auth_blueprint.route('/admin', methods=['POST'])
@login_required
def admin_post():
    if not approve_access(current_user.role.name, 'admin'):
        abort(403)

    user_id = request.form.get("id")
    new_name = request.form.get("name")
    new_role = request.form.get("role")
    action = request.form.get("action")

    if user_id == current_user.id:
        return redirect(url_for('auth.admin'))

    if action == "Update":
        if update_user(user_id, new_name, new_role):
            return redirect(url_for('auth.admin'))
    elif action == "Delete":
        if delete_user(user_id):
            return redirect(url_for('auth.admin'))
    elif action == "Reset Password":
        default_password = "default_password"
        if update_user_password(user_id, generate_password_hash(default_password, method='sha256', salt_length=32)):
            return redirect(url_for('auth.admin'))

    return abort(400)


@auth_blueprint.route('/update', methods=['POST'])
def update_profile():
    new_name = request.form.get("name")
    new_password = request.form.get('password')

    if new_password:
        if not update_user_password(current_user.id,
                                           generate_password_hash(new_password, method='sha256', salt_length=32)):
            return abort(400)

    if not new_name == '' and not new_name == current_user.name:
        if not update_user_name(current_user.id, new_name):
            return abort(400)

    return redirect(url_for('main.home'))
