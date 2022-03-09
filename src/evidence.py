from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from src import models
from sqlalchemy.exc import SQLAlchemyError
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


@evidence_blueprint.route('/search/', methods=['GET', 'POST'])
@login_required
def search_post():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)

    employee_name_list = models.users_name()
    project_name_list = models.projects_name()
    criteria_name_list = models.get_all_criteria_name()

    if request.method == 'POST':

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

        session['id'] = id
        session['criteria'] = criteria
        session['project'] = project
        session['employee_name'] = employee_name
        session['create_time'] = create_time
        session['ledit_time'] = last_edit_time

        results = models.get_info_by_filter(criteria, project, employee_name, create_time, last_edit_time, id)
        result_list = results.paginate(page=1, per_page=8, error_out=False)

        if result_list.total == 0:
            flash('No result found.')
            return redirect(url_for('evidence.search'))

        else:

            return render_template('search.html', results=result_list, employee_names=employee_name_list,
                                   project_names=project_name_list, criteria_names=criteria_name_list)



    else:
        page = int(request.args.get('page', 1))

        id = session.get('id')
        criteria = session.get('criteria')
        project = session.get('project')
        employee_name = session.get('employee_name')
        create_time = session.get('create_time')
        last_edit_time = session.get('ledit_time')

        results = models.get_info_by_filter(criteria, project, employee_name, create_time, last_edit_time, id)
        result_list = results.paginate(page=page, per_page=8, error_out=False)
        return render_template('search.html', results=result_list, employee_names=employee_name_list,
                               project_names=project_name_list, criteria_names=criteria_name_list)


@evidence_blueprint.route('/upload')
@login_required
def upload():
    if not approve_access(current_user.role.name, 'upload'):
        abort(403)

    criteria_list = models.criteria_id_name()

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
        f = open(file_path, 'r')
        contents = f.read()
        if not contents:
            contents = " "
        try:
            models.add_evidence(evidence_name, project_name, description, contents, user_id, criteria_id)
        except SQLAlchemyError as e:
            flash("evidence upload fail due to file upload fail/evidence name repeat")
            return redirect(url_for('evidence.upload'))
        # return redirect(url_for('evidence.view', evidence_id=evidence_id))
    return redirect(url_for('evidence.upload'))


@evidence_blueprint.route('/view', methods=['GET'])
@login_required
def view():
    if not approve_access(current_user.role.name, 'view'):
        abort(403)

    evidence_id = request.args.get("evidence_id")
    evidence = models.get_evidence_info(evidence_id)
    linked_criteria = models.get_criteria_by_id(evidence['criteria_id'])
    creator = models.get_user_by_id(evidence['user_id'])

    can_approve = approve_access(current_user.role.name, 'approve_evidence')

    return render_template('view.html', evidence=evidence, linked_criteria=linked_criteria, creator=creator,
                           can_approve=can_approve)


@evidence_blueprint.route('/update_evidence', methods=['POST'])
@login_required
def update_evidence():
    action = request.form.get('action')
    evidence_id = request.form.get("evidence_id")

    if action == 'Submit Changes':
        if not approve_access(current_user.role.name, 'update_evidence'):
            abort(403)

        new_description = request.form.get("description")
        file = request.files.get('file_upload')

        file_dir = os.path.join(os.getcwd(), UPLOAD_FOLDER)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        if file:
            file_path = os.path.join(file_dir, file.filename)
            file.save(file_path)
            f = open(file_path, 'r')
            contents = f.read()
            if not contents:
                contents = " "
            try:
                models.update_evidence_with_file(evidence_id, new_description, contents)
            except SQLAlchemyError as e:
                flash("evidence upload fail due to file upload fail/evidence name repeat")
        else:
            models.update_evidence(evidence_id, new_description)
    else:
        if not approve_access(current_user.role.name, 'approve_evidence'):
            abort(403)

        if action == 'Approve':
            models.update_evidence_status(evidence_id, 1)
        elif action == 'Disapprove':
            models.update_evidence_status(evidence_id, -1)
        elif action == 'Return to Pending':
            models.update_evidence_status(evidence_id, 0)

    return redirect(url_for('evidence.view', evidence_id=evidence_id))


@evidence_blueprint.route('/delete_evidence', methods=['POST'])
@login_required
def delete_evidence():
    evidence_id = request.form.get("evidence_id")
    evidence_to_delete = models.get_evidence_info(evidence_id)

    if not approve_access(current_user.role.name, 'delete_evidence') or not evidence_to_delete[
                                                                                'user_id'] == current_user.id:
        abort(403)

    if models.delete_evidence(evidence_id):
        return redirect(url_for('main.home'))

    abort(400)
