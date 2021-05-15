from flask import jsonify, request
from app import db
from sqlalchemy import func
from app.models import Quiz, QuestionLog, Question
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
    proportions = Quiz.get_quiz_score_distribution()
    return jsonify(proportions)


@bp.route('/getQuestionCount', methods=['POST', 'GET'])
def get_question_count():
    question_count = Question.get_question_count()
    return jsonify(question_count)


@bp.route('/getQuizzesByUser', methods=['POST', 'GET'])
def get_quizzes_by_user():
    quizzes = []
    for q in Quiz.get_user_quiz(current_user.id):
        quizzes.append(q.to_dict())
    return jsonify(quizzes)


@bp.route('/getQuestionsByQuiz/<quiz_id>', methods=['GET'])
def get_questions_by_quiz(quiz_id):
    q_id = quiz_id
    questions = []
    for q in QuestionLog.get_selected_questions_by_quiz(q_id):
        q = {
            'QuestionLog': q.QuestionLog.to_dict(),
            'QuestionAnswer': q.QuestionAnswer.to_dict(),
            'Question': q.Question.to_dict()
        }
        questions.append(q)
    return jsonify(questions)
