from flask import jsonify, g, abort
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from flask_login import current_user


@bp.route('/user/<username>', methods=['GET'])
@token_auth.login_required
def get_user_by_name(username):
    if current_user.username != username:
        abort(403)
    return jsonify(User.query.get_or_404(username).to_dict())
