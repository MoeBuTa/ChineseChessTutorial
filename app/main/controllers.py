import random

from flask import render_template, flash, redirect, url_for, jsonify
from sqlalchemy import func, desc, asc
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial, Assessment, AssessmentLog, Quiz
from app.data import add_tutorial_data, addAssessment
from sqlalchemy.orm import class_mapper
from app import moment
from datetime import datetime


class IndexController:

    @staticmethod
    def index():
        if not Tutorial.query.all():
            add_tutorial_data()
        if not Assessment.query.all():
            addAssessment()
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
            flash('Welcome back to <b>Tutorial section, ' +
                  current_user.username + '!</b>' +
                  ' last seen on <b>page' +
                  str(current_tutorial.tutorial_num) + '</b>, ' +
                  current_user.last_tutorial_read_time.strftime("%H:%M:%S, %d %b  %Y"))

        return render_template('tutorial.html', title='Chinese chess tutorial', current_tutorial=current_tutorial,
                               tutorial_count=tutorial_count)

    # query switched tutorial by num and save progress
    @staticmethod
    def tutorial_switch(target_tutorial_num):
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
        assessments = Assessment.query.all()
        selected_assessments = []
        quiz_id = 0
        # check if database has assessments available
        if assessments:
            assess_log = []

            # check if current user has unfinished quiz
            quiz = Quiz.query.filter(Quiz.user_id == current_user.id and Quiz.status == 0).first()
            if not quiz:
                quiz = Quiz(user_id=current_user.id, last_assessment_edit_time=datetime.now())
                db.session.add(quiz)
                db.session.flush()
                quiz_id = quiz.id
                j = 0
                for i in random.sample(range(1, len(assessments)), 6):
                    j += 1
                    assess = AssessmentLog(assessment_id=assessments[i].id,
                                           current_assessment_num=j, quiz_id=quiz_id)
                    selected_assess = {
                        "Assessment": assessments[i],
                        "AssessmentLog": assess
                    }
                    selected_assessments.append(selected_assess)
                    db.session.add(assess)
                db.session.commit()
            else:
                selected_assessments = Assessment.query.join(
                    AssessmentLog, (Assessment.id == AssessmentLog.assessment_id)).filter(
                    AssessmentLog.quiz_id == quiz.id).order_by(
                    asc(AssessmentLog.current_assessment_num)
                ).add_entity(AssessmentLog).all()
                quiz_id = selected_assessments[0].AssessmentLog.quiz_id
                flash(
                    'Welcome back to <b>Quiz section, ' + current_user.username + '</b>!' +
                    ' you have unfinished quiz! &nbsp;last seen on' ': ' +
                    quiz.last_assessment_edit_time.strftime("%H:%M:%S, %d %b  %Y"))
        else:
            flash("no assessments available in the database! ")
        return render_template('quiz1.html', title='Chinese chess Assessments',
                               selected_assessments=selected_assessments, quiz_id=quiz_id)

    @staticmethod
    def save_assessments_progress(selected_answer, assessment_log_id, quiz_id):
        assessment_log = AssessmentLog.query.get(assessment_log_id)
        assessment_log.selected_answer = selected_answer
        db.session.commit()
        quiz = Quiz.query.get(quiz_id)
        quiz.last_assessment_edit_time = datetime.now()
        db.session.commit()
        return "success"
