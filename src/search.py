from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user


from src import models
from src.include.access_controller import approve_access

search_blueprint = Blueprint('search', __name__)


@search_blueprint.route('/search')
@login_required
def search():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)
    employee_name_list = models.users_name()
    project_name_list = models.projects_name()
    criteria_name_list = models.criterias_name()

    return render_template('search.html', employee_names = employee_name_list, project_names = project_name_list ,criteria_names = criteria_name_list)


@search_blueprint.route('/search', methods=['POST'])
@login_required
def search_post():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)

    id = request.form.get('id')
    criteria = request.form.get('criteria')
    project = request.form.get('project')
    employee_name = request.form.get('employee_name')
    create_time = request.form.get('create_time')
    last_edit_time = request.form.get('ledit_time')

    if len(id) == 0:
        id = None

    if len(criteria) == 0:
        criteria = None

    if len(project) == 0:
        project = None

    if len(employee_name) == 0:
        employee_name = None

    if len(create_time) == 0:
        create_time = None

    if len(last_edit_time) == 0:
        last_edit_time = None


    results = models.get_info_by_filter(criteria,project,employee_name,create_time,last_edit_time,id)

    employee_name_list = models.users_name()
    project_name_list = models.projects_name()
    criteria_name_list = models.criterias_name()

    if not results:
        flash('No result found.')
        return redirect(url_for('search.search'))

    else:
        return render_template('search.html', results=results, employee_names=employee_name_list,
                               project_names=project_name_list, criteria_names=criteria_name_list)








