from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from src import models
from src.include.access_controller import approve_access

upload_blueprint = Blueprint('upload', __name__)


@upload_blueprint.route('/upload')
@login_required
def upload():
    if not approve_access(current_user.role.name, 'upload'):
        abort(403)

    return render_template('upload.html')


@upload_blueprint.route('/upload', methods=['POST'])
@login_required
def upload_post():
    if not approve_access(current_user.role.name, 'upload'):
        abort(403)

    evidence_name = request.form.get('evidence_name')
    models.add_evidence(evidence_name)
    return render_template('upload.html')
