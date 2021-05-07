from app.main.controllers import IndexController, TutorialController, StoryController, QuestionController
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


@bp.route('/tutorialSwitch', methods=['POST'])
@login_required
def tutorial_switch():
    target_tutorial_num = request.form.get('target_tutorial_num')
    return TutorialController.tutorial_switch(target_tutorial_num)


@bp.route('/questionsInfo')
@login_required
def questions_info():
    return QuestionController.questions_info()


@bp.route('/questions')
@login_required
def questions():
    return QuestionController.questions()


@bp.route('/saveQuestionsProgress', methods=['POST'])
@login_required
def save_questions_progress():
    selected_answer = request.form.get('selected_answer')
    question_log_id = request.form.get('question_log_id')
    quiz_id = request.form.get('quiz_id')
    return QuestionController.save_questions_progress(selected_answer, question_log_id, quiz_id)


@bp.route('/submitQuestions', methods=['POST'])
@login_required
def submit_questions():
    return QuestionController.submit_questions(request.form)