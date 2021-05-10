from flask import jsonify, request
from app import db
from sqlalchemy import func
from app.models import Quiz, QuestionLog
from app.api import bp
from app.api.errors import bad_request
from flask_login import current_user, login_required


@bp.route('/saveQuestionsProgress', methods=['POST'])
@login_required
def save_questions_progress():
    data = request.form or {}
    if 'selected_answer' not in data or 'question_log_id' not in data or 'quiz_id' not in data:
        return bad_request('lack of necessary fields!')
    question_log = QuestionLog.query.get(data['question_log_id'])
    question_log.save_question_progress(data['selected_answer'])
    quiz = Quiz.query.get(data['quiz_id'])
    quiz.update_quiz_edit_time()
    return "success", 200


@bp.route('/getDataForPieChart', methods=['POST'])
def get_data_for_pie_chart():
    count_score_below_forty = db.session.query(func.count(Quiz.id)).filter(Quiz.total_score < 40).scalar()
    count_score_between_forty_and_eighty = db.session.query(func.count(Quiz.id)).filter(
        Quiz.total_score >= 40, Quiz.total_score < 80).scalar()
    count_score_above_eighty = db.session.query(func.count(Quiz.id)).filter(
        Quiz.total_score >= 80).scalar()
    count_total = Quiz.get_quizzes_count()

    proportions = {
        "count_score_below_forty": count_score_below_forty,
        "count_score_between_forty_and_eighty": count_score_between_forty_and_eighty,
        "count_score_above_eighty": count_score_above_eighty,
        "count_total": count_total
    }
    return jsonify(proportions)