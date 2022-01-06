from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from src.include.access_controller import approve_access

search_blueprint = Blueprint('search', __name__)


@search_blueprint.route('/search')
@login_required
def search():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)

    return render_template('search.html')


@search_blueprint.route('/search', methods=['POST'])
@login_required
def search_post():
    if not approve_access(current_user.role.name, 'search'):
        abort(403)

    return render_template('search.html')
