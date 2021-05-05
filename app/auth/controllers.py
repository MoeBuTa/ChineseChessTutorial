from flask import render_template, flash, redirect, url_for
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial
from datetime import datetime


class UserController:

    @staticmethod
    def login_and_register():

        # if current_user.is_authenticated:
        #     return redirect(url_for('main.index'))

        # create login form
        loginForm = LoginForm()
        if loginForm.login_submit.data and loginForm.validate():
            user = User.query.filter_by(username=loginForm.login_username.data).first()
            if user is None or not user.check_password(loginForm.login_password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login_and_register'))
            login_user(user, remember=loginForm.remember_me.data)
            return redirect(url_for('main.index'))

        # create register form
        registrationForm = RegistrationForm()
        if registrationForm.registration_submit.data:
            flash("Congratulations, you are now a registered user!")
        return render_template('loginAndRegister.html', title='Sign In/up',
                               loginForm=loginForm, registrationForm=registrationForm)

    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for('main.index'))

    @staticmethod
    def register_validation(register_username, email, register_password):

        response = {
            "action": 0,
            "msg": '',
            "target": ''
        }

        # validate username
        check_username = User.query.filter_by(username=register_username).first()
        if check_username is not None:
            response["msg"] = 'Please use a different username!'
            response["target"] = "register_username"
            return response

        # validate email
        check_email = User.query.filter_by(email=email).first()
        if check_email is not None:
            response["msg"] = 'Please use a different email address!'
            response["target"] = "email"
            return response

        # add user to database
        else:
            user = User(username=register_username, email=email, register_time=datetime.now())
            user.set_password(register_password)
            db.session.add(user)
            db.session.commit()
            registered_user = User.query.filter_by(username=register_username).first()
            registered_user.save_tutorial_progress(1)
            response["action"] = 1
            return response
