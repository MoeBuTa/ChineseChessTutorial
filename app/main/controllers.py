from flask import render_template, flash, redirect, url_for
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User


class IndexController:

    @staticmethod
    def index():
        return render_template('index.html', title='Chinese Chess')


class TutorialController:

    @staticmethod
    def tutorial():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login_and_register'))
        return render_template('rule.html', title='Chinese chess tutorial')
