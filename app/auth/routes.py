from app.auth import bp
from app.auth.controllers import UserController
from flask import request


@bp.route('/loginAndRegister', methods=['GET', 'POST'])
def login_and_register():
    return UserController.login_and_register()


@bp.route('/logout')
def logout():
    return UserController.logout()


@bp.route('/registerValidation', methods=['GET', 'POST'])
def register_validation():
    register_username = request.form.get("register_username")
    email = request.form.get("email")
    register_password = request.form.get("register_password")
    return UserController.register_validation(register_username, email, register_password)

