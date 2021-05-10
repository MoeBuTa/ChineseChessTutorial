from flask import jsonify, g, abort, request
from app.models import Tutorial, TutorialProgress
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/tutorial/<tutorial_num>', methods=['GET'])
@token_auth.login_required
def get_tutorial_by_num(tutorial_num):
    return jsonify(Tutorial.query_by_num(tutorial_num))


@bp.route('/tutorialSwitch', methods=['POST'])
@token_auth.login_required
def switch_tutorial():
    data = request.get_json() or {}
    if 'target_tutorial_num' not in data:
        return bad_request('must include tutorial_num field!')
    target_tutorial = Tutorial.query.filter_by(tutorial_num=data['target_tutorial_num']).first()
    TutorialProgress.save_tutorial_progress(g.current_user.id, data['target_tutorial_num'])
    return jsonify(target_tutorial.to_dict())
