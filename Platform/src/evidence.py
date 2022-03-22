from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from Platform import *
from sqlalchemy.exc import SQLAlchemyError
from Platform.src.include.access_controller import approve_access
import os

evidence_blueprint = Blueprint('evidence', __name__)
UPLOAD_FOLDER = 'upload_files'


@evidence_blueprint.route('/search')
@login_required
def search():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)
    employee_name_list = users_name()
    project_name_list = projects_name()
    criteria_name_list = get_all_criteria_name()

    return render_template('search.html', employee_names=employee_name_list, project_names=project_name_list,
                           criteria_names=criteria_name_list)


@evidence_blueprint.route('/search/', methods=['GET', 'POST'])
@login_required
def search_post():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)

    employee_name_list = users_name()
    project_name_list = projects_name()
    criteria_name_list = get_all_criteria_name()

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

        results = get_info_by_filter(criteria, project, employee_name, create_time, last_edit_time, id)
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

        results = get_info_by_filter(criteria, project, employee_name, create_time, last_edit_time, id)
        result_list = results.paginate(page=page, per_page=8, error_out=False)
        return render_template('search.html', results=result_list, employee_names=employee_name_list,
                               project_names=project_name_list, criteria_names=criteria_name_list)


@evidence_blueprint.route('/upload')
@login_required
def upload():
    if not approve_access(current_user.role.name, 'upload'):
        abort(403)

    criteria_list = criteria_id_name()

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
        f = open(file_path, 'rb')
        contents = f.read()
        if not contents:
            contents = " "
        try:
            id = add_evidence(evidence_name, project_name, description, contents, user_id, criteria_id)
        except SQLAlchemyError as e:
            flash("evidence upload fail due to file upload fail/evidence name repeat")
            return redirect(url_for('evidence.upload'))
        # return redirect(url_for('evidence.view', evidence_id=evidence_id))
    return redirect(url_for('evidence.view', evidence_id=id))


@evidence_blueprint.route('/view', methods=['GET'])
@login_required
def view():
    if not approve_access(current_user.role.name, 'view'):
        abort(403)

    evidence_id = request.args.get("evidence_id")
    evidence = get_evidence_info(evidence_id)
    linked_criteria = get_criteria_by_id(evidence['criteria_id'])
    creator = get_user_by_id(evidence['user_id'])

    can_delete = approve_access(current_user.role.name, 'delete_evidence')
    can_approve = approve_access(current_user.role.name, 'approve_evidence')
    can_update = approve_access(current_user.role.name, 'update_evidence')

    return render_template('view.html', evidence=evidence, linked_criteria=linked_criteria, creator=creator,
                           can_approve=can_approve, can_delete=can_delete, can_update=can_update)


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
            f = open(file_path, 'rb')
            contents = f.read()
            if not contents:
                contents = " "
            try:
                update_evidence_with_file(evidence_id, new_description, contents)
                update_evidence_status(evidence_id, 0)
            except SQLAlchemyError as e:
                flash("evidence upload fail due to file upload fail/evidence name repeat")
        else:
            update_evidence_des(evidence_id, new_description)
            update_evidence_status(evidence_id, 0)

    elif action == 'Delete':
        if delete_evidence(evidence_id):
            return redirect(url_for('main.home'))
    else:
        if not approve_access(current_user.role.name, 'approve_evidence'):
            abort(403)

        if action == 'Approve':
            update_evidence_status(evidence_id, 1)
        elif action == 'Disapprove':
            update_evidence_status(evidence_id, -1)
        elif action == 'Return to Pending':
            update_evidence_status(evidence_id, 0)

    return redirect(url_for('evidence.view', evidence_id=evidence_id))


@evidence_blueprint.route('/delete_evidence', methods=['POST'])
@login_required
def evidence_delete():
    evidence_id = request.form.get("evidence_id")
    evidence_to_delete = get_evidence_info(evidence_id)

    if not approve_access(current_user.role.name, 'delete_evidence') or not evidence_to_delete[
                                                                                'user_id'] == current_user.id:
        abort(403)

    if delete_evidence(evidence_id):
        return redirect(url_for('main.home'))

    abort(400)
