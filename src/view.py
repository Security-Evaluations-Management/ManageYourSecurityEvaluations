from flask import Blueprint, render_template, request
from flask_login import login_required
import models

view_blueprint = Blueprint('view', __name__)


@view_blueprint.route('/view/<evidence_id>', methods=['POST', 'GET'])
@login_required
def view(evidence_id):
    evidence = models.get_evidence_info(evidence_id)
    content = 'Here is evidence'

    return render_template('view.html', evidence=evidence)
