from flask import render_template, flash, redirect, url_for, jsonify
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial, Assessment, AssessmentLog, Quiz, AssessmentAnswer
from app.data import add_tutorial_data, addAssessment
from sqlalchemy.orm import class_mapper
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
        tutorial_count = Tutorial.get_tutorial_count()
        if current_user.last_tutorial_read_time:
            flash('Welcome back to <b>Tutorial section, ' +
                  current_user.username + '!</b>' +
                  ' last seen on <b>page' +
                  str(current_tutorial.tutorial_num) + '</b>, ' +
                  current_user.last_tutorial_read_time.strftime("%d %b  %Y, %H:%M:%S"))

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

            # check if current user has unfinished quiz
            quiz = Quiz.query.filter(Quiz.status == 0 and Quiz.user_id == current_user.id).first()
            if not quiz:
                quiz = Quiz(user_id=current_user.id,
                            start_assessment_time=datetime.now(),
                            status=0,
                            last_assessment_edit_time=datetime.now())
                selected_assessments = Quiz.addNewQuiz(quiz, assessments)

            else:
                selected_assessments = Assessment.get_selected_assessment(quiz.id)
                flash(
                    'Welcome back to <b>Quiz section, ' + current_user.username + '</b>!' +
                    ' you have <b>unfinished quiz!</b> &nbsp;last seen on' ': ' +
                    quiz.last_assessment_edit_time.strftime("%d %b  %Y, %H:%M:%S"))
            quiz_id = selected_assessments[0].AssessmentLog.quiz_id

        else:
            flash("no assessments available in the database! ")

        return render_template('quiz1.html', title='Chinese chess Assessments',
                               selected_assessments=selected_assessments, quiz_id=quiz_id)

    @staticmethod
    def save_assessments_progress(selected_answer, assessment_log_id, quiz_id):
        assessment_log = AssessmentLog.query.get(assessment_log_id)
        assessment_log.save_assessment_progress(selected_answer)
        quiz = Quiz.query.get(quiz_id)
        quiz.update_quiz_edit_time()
        return "success"

    @staticmethod
    def submit_assessments(form):

        total_score = 0
        assessment_log_ids = form.keys()

        # update submitted answers
        selected_assessments = AssessmentLog.get_selected_assessment_answer(assessment_log_ids)
        quiz_id = selected_assessments[0].AssessmentLog.quiz_id

        # calculate quiz result
        for assess in selected_assessments:
            if assess.AssessmentAnswer.answer == assess.AssessmentLog.selected_answer:
                total_score += assess.AssessmentAnswer.score
                assess.AssessmentLog.correct = 1
            else:
                assess.AssessmentLog.correct = 0

        # update quiz info
        quiz = Quiz.query.get(quiz_id)
        if quiz.status == 0:
            quiz.submit_quiz(total_score)

        return render_template('quiz-feedback.html', title='feedback', selected_assessments=selected_assessments,
                               quiz=quiz)
