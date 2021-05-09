from flask import render_template, flash, redirect, url_for, jsonify
from app import db
from flask_login import current_user
from app.models import Tutorial, Question, QuestionLog, Quiz, TutorialProgress
from app.data import add_tutorial_data, addQuestion
from sqlalchemy.orm import class_mapper
from datetime import datetime
from sqlalchemy import func
import numpy as np


class IndexController:

    @staticmethod
    def index():
        if not Tutorial.query.all():
            add_tutorial_data()
        if not Question.query.all():
            addQuestion()
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
        current_tutorial = Tutorial.query_tutorial(current_user.id)
        current_tutorial_progress = TutorialProgress.query_tutorial_progress(current_user.id)
        tutorial_count = Tutorial.get_tutorial_count()
        if current_tutorial_progress.last_tutorial_read_time:
            flash('Welcome back to <b>Tutorial Section Page&nbsp;' +
                  str(current_tutorial_progress.read_tutorial_num) + ', ' +
                  current_user.username + '!</b>' +
                  ' &nbsp;&nbsp; last seen on: ' +
                  current_tutorial_progress.last_tutorial_read_time.strftime("%d %b  %Y, %H:%M:%S"))
        else:
            current_tutorial_progress.set_first_read_time()

        return render_template('tutorial.html', title='Chinese chess tutorial', current_tutorial=current_tutorial,
                               tutorial_count=tutorial_count)

    # query switched tutorial by num and save progress
    @staticmethod
    def tutorial_switch(target_tutorial_num):
        target_tutorial = Tutorial.query.filter_by(tutorial_num=target_tutorial_num).first()
        TutorialProgress.save_tutorial_progress(current_user.id, target_tutorial_num)
        return jsonify(IndexController.serialize(target_tutorial))


class StoryController:

    @staticmethod
    def story():
        return render_template('story.html', title='The Story of Chinese chess')


class QuestionController:

    @staticmethod
    def questions_info():
        # check if current user has unfinished quiz
        quiz = Quiz.query.filter(Quiz.status == 0 and Quiz.user_id == current_user.id).first()
        if quiz:
            return QuestionController.questions()
        return render_template('quizInfo.html', title='Chinese chess questions')

    @staticmethod
    def questions():
        questions_in_db = Question.query.all()
        selected_questions = []
        quiz_id = 0
        # check if database has questions available
        if questions_in_db:

            # check if current user has unfinished quiz
            quiz = Quiz.query.filter(Quiz.status == 0 and Quiz.user_id == current_user.id).first()
            if not quiz:
                quiz = Quiz(user_id=current_user.id,
                            start_question_time=datetime.now(),
                            status=0,
                            last_question_edit_time=datetime.now())
                selected_questions = Quiz.addNewQuiz(quiz, questions_in_db)

            else:
                selected_questions = Question.get_selected_question(quiz.id)
                flash(
                    'Welcome back to <b>Quiz Section, ' + current_user.username + '</b>!' +
                    ' you have <b>unfinished quiz!</b> &nbsp;&nbsp;last seen on: ' +
                    quiz.last_question_edit_time.strftime("%d %b  %Y, %H:%M:%S"))
            quiz_id = selected_questions[0].QuestionLog.quiz_id

        else:
            flash("no questions available in the database! ")

        return render_template('quiz.html', title='Chinese chess questions',
                               selected_questions=selected_questions, quiz_id=quiz_id)

    @staticmethod
    def save_questions_progress(selected_answer, question_log_id, quiz_id):
        question_log = QuestionLog.query.get(question_log_id)
        question_log.save_question_progress(selected_answer)
        quiz = Quiz.query.get(quiz_id)
        quiz.update_quiz_edit_time()
        return "success"

    @staticmethod
    def submit_questions(form):
        total_score = 0
        question_log_ids = form.keys()
        # update submitted answers
        selected_questions = QuestionLog.get_selected_question_answer(question_log_ids)
        quiz_id = selected_questions[0].QuestionLog.quiz_id

        # calculate quiz result
        for quest in selected_questions:
            if quest.QuestionAnswer.answer == quest.QuestionLog.selected_answer:
                total_score += quest.QuestionAnswer.score
                quest.QuestionLog.correct = 1
            else:
                quest.QuestionLog.correct = 0

        # update quiz info
        quiz = Quiz.query.get(quiz_id)
        if quiz.status == 0:
            quiz.submit_quiz(total_score)

        return render_template('quiz-feedback.html', title='feedback', selected_questions=selected_questions,
                               quiz=quiz)


class GeneralController:

    @staticmethod
    def general_view():
        # GeneralController.get_data_for_pie_chart()
        return render_template('general.html', title='general view')

    @staticmethod
    def get_data_for_pie_chart():
        count_score_below_forty = db.session.query(func.count(Quiz.id)).filter(Quiz.total_score <= 40).scalar()
        count_score_between_forty_and_eighty = db.session.query(func.count(Quiz.id)).filter(
            Quiz.total_score > 40, Quiz.total_score < 80).scalar()
        count_score_above_eighty = db.session.query(func.count(Quiz.id)).filter(
            Quiz.total_score >= 80).scalar()
        count_total = Quiz.get_quizzes_count()

        proportions = {
            "count_score_below_forty": count_score_below_forty,
            "count_score_between_forty_and_eighty": count_score_between_forty_and_eighty,
            "count_score_above_eighty": count_score_above_eighty,
            "count_total": count_total
        }
        return jsonify(proportions)

    @staticmethod
    def get_data_for_area_chart():
        tutorial_progresses = TutorialProgress.query.all()
        tutorial_count = Tutorial.get_tutorial_count()
        tutorial_time_list = {}
        tutorial_average_time = [['P' + str(x), 0] for x in range(0, tutorial_count)]
        for tu in tutorial_progresses:
            if not tutorial_time_list.get(tu.read_tutorial_num):
                tutorial_time_list[tu.read_tutorial_num] = []
            tutorial_time_list[tu.read_tutorial_num].append(tu.time_duration)
        for k, v in tutorial_time_list.items():
            tutorial_average_time[k - 1] = ['P' + str(k), np.mean(v)]

        return jsonify(tutorial_average_time)
