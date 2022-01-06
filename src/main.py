from flask import Blueprint, render_template
from flask_login import current_user

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def home():
    return render_template('welcomePage.html', current_user=current_user)
