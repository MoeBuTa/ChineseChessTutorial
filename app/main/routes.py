from app.main.controllers import IndexController, TutorialController
from app.main import bp
from flask_login import login_required


@bp.route('/')
@bp.route('/index')
def index():
    return IndexController.index()


@bp.route('/tutorial')
@login_required
def tutorial():
    return TutorialController.tutorial()

