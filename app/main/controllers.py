import random

from flask import render_template, flash, redirect, url_for, jsonify
from sqlalchemy import func
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial, Ques
from app.data import add_tutorial_data, addQues
from sqlalchemy.orm import class_mapper
from app import moment


class IndexController:

    @staticmethod
    def index():
        if not Tutorial.query.all():
            add_tutorial_data()
        if not Ques.query.all():
            addQues()
        return render_template('index.html', title='Chinese Chess')

    @staticmethod
    def serialize(model):
        columns = [c.key for c in class_mapper(model.__class__).columns]
        return dict((c, getattr(model, c)) for c in columns)


class TutorialController:

    # render tutorial.html
    @staticmethod
    def tutorials():
        # authentication required
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login_and_register'))

        # query current tutorial progress
        current_tutorial = current_user.query_tutorial_progress()
        tutorial_count = db.session.query(func.count(Tutorial.id)).scalar()
        if current_user.last_tutorial_read_time:
            flash(
                'Welcome back ' + current_user.username + '!' +
                ' last seen on Tutorial ' +
                str(current_tutorial.tutorial_num) + ': ' +
                current_user.last_tutorial_read_time.strftime("%H:%M:%S, %d %b  %Y"))
        return render_template('tutorial.html', title='Chinese chess tutorial', current_tutorial=current_tutorial,
                               tutorial_count=tutorial_count)

    # query switched tutorial by num and save progress
    @staticmethod
    def tutorial_switch(target_tutorial_num):
        print(target_tutorial_num)
        target_tutorial = Tutorial.query.filter_by(tutorial_num=target_tutorial_num).first()
        current_user.save_tutorial_progress(target_tutorial.id)
        return jsonify(IndexController.serialize(target_tutorial))


class StoryController:

    @staticmethod
    def story():
        return render_template('story.html', title='The Story of Chinese chess')


class AssessmentController:

    @staticmethod
    def assessmentsInfo():
        return render_template('quiz.html', title='Chinese chess Assessments')

    @staticmethod
    def assessments():
        L1 = random.sample(range(1, 9), 7)
        ques = Ques.query.all()
        form = []
        if ques:
            for i in L1:
                form.append(ques[i])

        return render_template('quiz1.html', title='Chinese chess Assessments', form=form)
