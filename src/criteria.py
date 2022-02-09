from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.include.access_controller import approve_access
from src import models
import pandas as pd
from werkzeug.utils import secure_filename
import os


criteria_blueprint = Blueprint('criteria', __name__)
ALLOWED_EXTENTION = {'csv'}
UPLOAD_FOLDER_TEMP = 'temp_storage'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTION


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

    file = request.files.get('criteria_file')
    cname = request.form.get('criteria_name')
    description = request.form.get('description')

    if cname != "" and description != "":
        if not models.add_criteria(cname, description, current_user):
            flash("upload fail or criteria already exist")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_dir = os.path.join(os.getcwd(), UPLOAD_FOLDER_TEMP)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file.save(os.path.join(file_dir, filename))

        file.stream.seek(0)
        dataframe = pd.read_csv(file)
        for index, row in dataframe.iterrows():
            print(row['name'] + "," + row['description'])
            if not models.add_criteria(row['name'], row['description'], current_user):
                flash("upload fail or criteria already exist")

    return redirect(url_for('criteria.criteria'))


@criteria_blueprint.route('/criteria/delete', methods=['POST'])
@login_required
def criteria_delete_post():
    if not approve_access(current_user.role.name, 'criteria_modification'):
        abort(403)

    criteria_to_remove = request.form.get("criteria_to_remove_id")
    if models.remove_criteria(criteria_to_remove):
        return redirect(url_for('criteria.criteria'))

    return abort(400)
