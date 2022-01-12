from flask import Blueprint, abort, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from src.include.access_controller import approve_access
from src import models

criteria_blueprint = Blueprint('criteria', __name__)


@criteria_blueprint.route('/criteria')
@login_required
def criteria():
    if not approve_access(current_user.role.name, 'criteria'):
        abort(403)

    criteria_list = models.get_all_criteria()
    allow_modification = approve_access(current_user.role.name, 'criteria_modification')

    return render_template('criteria.html', criteria_list=criteria_list, allow_modification=allow_modification)


@criteria_blueprint.route('/criteria/creation', methods=['POST'])
@login_required
def criteria_creation_post():
    if not approve_access(current_user.role.name, 'criteria_modification'):
        abort(403)

    new_criteria_name = request.form.get("new_criteria_name")
    new_criteria_description = request.form.get("new_criteria_description")
    if models.add_criteria(new_criteria_name, new_criteria_description, current_user):
        return redirect(url_for('criteria.criteria'))

    return abort(400)


@criteria_blueprint.route('/criteria/delete', methods=['POST'])
@login_required
def criteria_delete_post():
    if not approve_access(current_user.role.name, 'criteria_modification'):
        abort(403)

    criteria_to_remove = request.form.get("criteria_to_remove_id")
    if models.remove_criteria(criteria_to_remove):
        return redirect(url_for('criteria.criteria'))

    return abort(400)
