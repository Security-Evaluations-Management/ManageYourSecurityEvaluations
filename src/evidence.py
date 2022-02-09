from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src import models
from src.include.access_controller import approve_access
import os


evidence_blueprint = Blueprint('evidence', __name__)
UPLOAD_FOLDER = 'upload_files'


@evidence_blueprint.route('/search')
@login_required
def search():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)
    employee_name_list = models.users_name()
    project_name_list = models.projects_name()
    criteria_name_list = models.get_all_criteria_name()

    return render_template('search.html', employee_names=employee_name_list, project_names=project_name_list,
                           criteria_names=criteria_name_list)


@evidence_blueprint.route('/search', methods=['POST'])
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

    results = models.get_info_by_filter(criteria, project, employee_name, create_time, last_edit_time, id)

    employee_name_list = models.users_name()
    project_name_list = models.projects_name()
    criteria_name_list = models.get_all_criteria_name()

    if not results:
        flash('No result found.')
        return redirect(url_for('evidence.search'))

    else:
        return render_template('search.html', results=results, employee_names=employee_name_list,
                               project_names=project_name_list, criteria_names=criteria_name_list)


@evidence_blueprint.route('/upload')
@login_required
def upload():
    if not approve_access(current_user.role.name, 'upload'):
        abort(403)

    criteria_list = models.criteria_id_name()
    print(criteria_list)

    return render_template('upload.html', criteria_list=criteria_list)


@evidence_blueprint.route('/upload', methods=['POST'])
@login_required
def upload_post():
    if not approve_access(current_user.role.name, 'upload'):
        abort(403)

    user_id = current_user.get_id()
    evidence_name = request.form.get('ev_name')
    project_name = request.form.get('proj_name')
    description = request.form.get('description')
    criteria_id = request.form.get('criteria')
    file = request.files.get('file_upload')

    file_dir = os.path.join(os.getcwd(), UPLOAD_FOLDER)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if file:
        file_path = os.path.join(file_dir, file.filename)
        file.save(file_path)
        f = open(file_path,'r')
        contents = f.read()
        models.add_evidence(evidence_name, project_name, description, contents, user_id, criteria_id)

        return redirect(url_for('view.view'))
    else:
        flash("file not upload")
        return redirect(url_for('evidence.upload'))
