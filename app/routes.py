from app import app
from app.controllers import IndexController, UserController


@app.route('/')
@app.route('/index')
def index():
    return IndexController.index()


@app.route('/loginAndRegister', methods=['GET', 'POST'])
def login_and_register():
    return UserController.login_and_register()


