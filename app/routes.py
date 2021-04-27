from app import app
from app.controllers import IndexController, UserController, TutorialController


@app.route('/')
@app.route('/index')
def index():
    return IndexController.index()


@app.route('/loginAndRegister', methods=['GET', 'POST'])
def login_and_register():
    return UserController.login_and_register()


@app.route('/logout')
def logout():
    return UserController.logout()


@app.route('/tutorial')
def tutorial():
    return TutorialController.tutorial()
