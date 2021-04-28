from app import app
from app.controllers import IndexController, UserController, TutorialController
from flask_login import login_required


@app.route('/')
@app.route('/index')
def index():
    return IndexController.index()


@app.route('/loginAndRegister', methods=['GET', 'POST'])
def login_and_register():
    return UserController.login_and_register()


@app.route('/logout')
@login_required
def logout():
    return UserController.logout()


@app.route('/tutorial')
@login_required
def tutorial():
    return TutorialController.tutorial()
