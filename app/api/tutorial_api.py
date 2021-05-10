from flask import jsonify,  request
from app.models import Tutorial, TutorialProgress
from app.api import bp
from app.api.errors import bad_request
from flask_login import current_user, login_required
import numpy as np


@bp.route('/tutorial/<tutorial_num>', methods=['GET'])
@login_required
def get_tutorial_by_num(tutorial_num):
    return jsonify(Tutorial.query_by_num(tutorial_num))


# query switched tutorial by num and save progress
@bp.route('/tutorialSwitch', methods=['POST'])
@login_required
def switch_tutorial():
    data = request.form or {}
    if 'target_tutorial_num' not in data:
        return bad_request('must include tutorial_num field!')
    target_tutorial = Tutorial.query.filter_by(tutorial_num=data['target_tutorial_num']).first()
    TutorialProgress.save_tutorial_progress(current_user.id, data['target_tutorial_num'])
    return jsonify(target_tutorial.to_dict())


@bp.route('/getDataForAreaChart', methods=['POST'])
def get_data_for_area_chart():
    tutorial_progresses = TutorialProgress.query.all()
    tutorial_count = Tutorial.get_tutorial_count()
    tutorial_time_list = {}
    tutorial_average_time = [['P' + str(x), 0] for x in range(0, tutorial_count)]
    for tu in tutorial_progresses:
        if not tutorial_time_list.get(tu.read_tutorial_num):
            tutorial_time_list[tu.read_tutorial_num] = []
        tutorial_time_list[tu.read_tutorial_num].append(tu.time_duration)
    for k, v in tutorial_time_list.items():
        tutorial_average_time[k - 1] = ['P' + str(k), np.mean(v)]
    return jsonify(tutorial_average_time)