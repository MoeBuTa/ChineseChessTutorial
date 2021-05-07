from flask import render_template, flash, redirect, url_for, jsonify
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Tutorial, Question, QuestionLog, Quiz, QuestionAnswer
from app.data import add_tutorial_data, addQuestion
from sqlalchemy.orm import class_mapper
from datetime import datetime


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
        current_tutorial = current_user.query_tutorial_progress()
        tutorial_count = Tutorial.get_tutorial_count()
        if current_user.last_tutorial_read_time:
            flash('Welcome back to <b>Tutorial Section Page&nbsp;' +
                  str(current_tutorial.tutorial_num) + ', ' +
                  current_user.username + '!</b>' +
                  ' &nbsp;&nbsp; last seen on: ' +
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
        print(form)
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
        return render_template('general.html', title='general view')

