from app.auth import bp
from app.auth.controllers import UserController


@bp.route('/loginAndRegister', methods=['GET', 'POST'])
def login_and_register():
    return UserController.login_and_register()


@bp.route('/logout')
def logout():
    return UserController.logout()

