from flask import Blueprint, render_template, request
from flask_login import login_required

view_blueprint = Blueprint('view', __name__)


@view_blueprint.route('/view', methods=['POST'])
@login_required
def view():
    file_name = request.form.get('file_name')

    content = 'Here is evidence'
    # content = getContent(fileName, current_user) [getContent involve check privilege]
    # if content = false
    # display warning message
    # else
    # display content

    return render_template('view.html', content=content)
