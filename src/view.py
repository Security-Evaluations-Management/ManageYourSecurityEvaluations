from flask import Blueprint, render_template, request
from flask_login import login_required

view_blueprint = Blueprint('view', __name__)


@view_blueprint.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    # evidence = models.get_evidence_info(evidence_id)
    content = 'Here is evidence'

    return render_template('view.html', content=content)
