from flask import jsonify, abort, request
from app.models import User
from app.api import bp
from app.api.errors import bad_request
from flask_login import current_user, login_required
from datetime import datetime


@bp.route('/user/<username>', methods=['GET'])
@login_required
def get_user_by_name(username):
    if current_user.username != username:
        abort(403)
    return jsonify(User.query.get_or_404(username).to_dict())


@bp.route('/registerValidation', methods=['POST'])
def register_validation():
    data = request.form
    if 'register_username' not in data or 'email' not in data or 'register_password' not in data:
        return bad_request('must include all user fields!'), 400
    user = User(username=data['register_username'], email=data['email'], register_time=datetime.now())
    return user.register_validation(data['register_password'])


@bp.route('/getUserCount', methods=['POST', 'GET'])
def get_user_count():
    user_count = User.get_user_count()
    return jsonify(user_count)