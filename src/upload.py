from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from src import models
from src.include.access_controller import approve_access
import os

upload_blueprint = Blueprint('upload', __name__)
UPLOAD_FOLDER = 'upload_files'


@upload_blueprint.route('/upload')
@login_required
def upload():
    if not approve_access(current_user.role.name, 'upload'):
        abort(403)

    #criteria_list = models.
    criteria_list = [1, 2, 3, 4, 5]

    return render_template('upload.html', criteria_list=criteria_list)


@upload_blueprint.route('/upload', methods=['POST'])
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
        models.add_evidence(evidence_name, project_name, description, file_path, user_id, criteria_id)

        return redirect(url_for('view.view'))
    else:
        flash("file not upload")
        return redirect(url_for('upload.upload'))
