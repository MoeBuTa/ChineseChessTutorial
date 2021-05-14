from app.main.controllers import IndexController, TutorialController, StoryController, QuestionController, \
    GeneralController, UserViewController
from app.main import bp
from flask_login import login_required
from flask import request


@bp.route('/')
@bp.route('/index')
def index():
    return IndexController.index()


@bp.route('/story')
def story():
    return StoryController.story()


@bp.route('/tutorials')
@login_required
def tutorials():
    return TutorialController.tutorials()


@bp.route('/questionsInfo')
@login_required
def questions_info():
    return QuestionController.questions_info()


@bp.route('/questions')
@login_required
def questions():
    return QuestionController.questions()


@bp.route('/submitQuestions', methods=['POST'])
@login_required
def submit_questions():
    return QuestionController.submit_questions(request.form)


@bp.route('/generalView')
def general_view():
    return GeneralController.general_view()


@bp.route('/userView')
def user_view():
    return UserViewController.user_view()


@bp.route('/selectedQuiz/<quiz_id>', methods=['GET'])
def selected_quiz(quiz_id):
    return UserViewController.selected_quiz(quiz_id)
