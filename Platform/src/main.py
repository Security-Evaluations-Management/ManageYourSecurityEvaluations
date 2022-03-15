from flask import Blueprint, render_template
from flask_login import current_user

from Platform import get_evidence_by_userid

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def home():
    if current_user.is_authenticated:
        evidence_list = get_evidence_by_userid(current_user.id)
        return render_template('welcomePage.html', current_user=current_user, evidence_list=evidence_list)

    return render_template('welcomePage.html', current_user=current_user)
