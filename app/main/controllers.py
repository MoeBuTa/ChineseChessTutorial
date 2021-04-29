from flask import render_template, flash, redirect, url_for
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial
from app.tutorial_data import add_tutorial_data


class IndexController:

    @staticmethod
    def index():
        if not Tutorial.query.all():
            add_tutorial_data()
        return render_template('index.html', title='Chinese Chess')


class TutorialController:

    @staticmethod
    def tutorial():
        # authentication required
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login_and_register'))

        # query current tutorial progress
        current_tutorial = current_user.query_tutorial_progress()

        return render_template('rule1.html', title='Chinese chess tutorial', current_tutorial = current_tutorial)

