from flask import render_template, flash, redirect, url_for
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial


class UserController:

    @staticmethod
    def login_and_register():

        if current_user.is_authenticated:
            return redirect(url_for('main.index'))

        # create login form
        loginForm = LoginForm()
        if loginForm.loginSubmit.data and loginForm.validate():
            user = User.query.filter_by(username=loginForm.username.data).first()
            if user is None or not user.check_password(loginForm.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login_and_register'))
            login_user(user, remember=loginForm.remember_me.data)
            return redirect(url_for('main.index'))

        # create register form
        registrationForm = RegistrationForm()
        if registrationForm.registrationSubmit.data and registrationForm.validate():
            user = User(username=registrationForm.username.data, email=registrationForm.email.data)
            user.set_password(registrationForm.password.data)
            db.session.add(user)
            db.session.commit()
            registered_user = User.query.filter_by(username=registrationForm.username.data).first()
            registered_user.save_tutorial_progress(1)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth.login_and_register'))
        return render_template('loginAndRegister.html', title='Sign In/up',
                               loginForm=loginForm, registrationForm=registrationForm)

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('main.index'))


