from flask import jsonify, abort
from app.models import User
from app.api import bp
from flask_login import current_user, login_required


@bp.route('/user/<username>', methods=['GET'])
@login_required
def get_user_by_name(username):
    if current_user.username != username:
        abort(403)
    return jsonify(User.query.get_or_404(username).to_dict())
