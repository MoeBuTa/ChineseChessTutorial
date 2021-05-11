from flask import render_template, flash, redirect, url_for
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User, TutorialProgress
from datetime import datetime


class UserController:

    @staticmethod
    def login_and_register():

        if current_user.is_authenticated:
            return redirect(url_for('main.index'))

        # create login form
        loginForm = LoginForm()
        # create register form
        registrationForm = RegistrationForm()

        if loginForm.login_submit.data and loginForm.validate():
            user = User.query.filter_by(username=loginForm.login_username.data).first()
            if user is None or not user.check_password(loginForm.login_password.data):
                flash('Invalid username or password')
            else:
                login_user(user, remember=loginForm.remember_me.data)
                current_user.get_token()
                return redirect(url_for('main.index'))

        if registrationForm.registration_submit.data:
            flash("Congratulations, you are now a registered user!")
        return render_template('loginAndRegister.html', title='Sign In/up',
                               loginForm=loginForm, registrationForm=registrationForm)

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('main.index'))
