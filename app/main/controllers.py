from flask import render_template, flash, redirect, url_for, jsonify
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial
from app.tutorial_data import add_tutorial_data
from sqlalchemy.orm import class_mapper


class IndexController:

    @staticmethod
    def index():
        if not Tutorial.query.all():
            add_tutorial_data()
        return render_template('index.html', title='Chinese Chess')

    @staticmethod
    def serialize(model):
        columns = [c.key for c in class_mapper(model.__class__).columns]
        return dict((c, getattr(model, c)) for c in columns)


class TutorialController:

    @staticmethod
    def tutorials():
        # authentication required
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login_and_register'))

        # query current tutorial progress
        current_tutorial = current_user.query_tutorial_progress()

        return render_template('tutorial.html', title='Chinese chess tutorial', current_tutorial=current_tutorial)

    @staticmethod
    def tutorial_switch(target_tutorial_id):
        target_tutorial = Tutorial.query.get(target_tutorial_id)
        current_user.save_tutorial_progress(target_tutorial_id)
        return jsonify(IndexController.serialize(target_tutorial))


class StoryController:

    @staticmethod
    def story():
        return render_template('story.html', title='The Story of Chinese chess')
