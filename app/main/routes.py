from app.main.controllers import IndexController, TutorialController, StoryController, AssessmentController
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


@bp.route('/assessmentsInfo')
@login_required
def assessmentsInfo():
    return AssessmentController.assessmentsInfo()


@bp.route('/assessments')
@login_required
def assessments():
    return AssessmentController.assessments()