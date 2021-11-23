from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from werkzeug.utils import secure_filename
from flask_login import login_required
import os

upload = Blueprint('upload', __name__)
UPLOAD_FOLDER = 'C:/Users/Nrx03/Desktop/4y_final_proj/test_pack'
ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    # check if the file upload is within the types allowed
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload.route('/upload')
# @login_required
def upload_table():
    return render_template('upload.html')


@upload.route('/upload', methods=['POST'])
def upload_post():
    if request.method == 'POST':
        evidence_name = request.form.get('ev_name')
        proj_name = request.form.get('proj_name')

        description = request.form.get('description')
        # if(description):

        file = request.files['file_upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

    return redirect(url_for("upload_table"))


@upload.route('/upload', methods=['GET', 'POST'])
def search():



