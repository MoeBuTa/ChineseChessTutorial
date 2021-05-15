from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.models import Tutorial, Question, QuestionLog, Quiz, TutorialProgress, User
from datetime import datetime
from tests import data


class IndexController:

    @staticmethod
    def index():
        if not Tutorial.query.all():
            data.add_data()
        return render_template('index.html', title='Chinese Chess')


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


class StoryController:

    @staticmethod
    def story():
        return render_template('story.html', title='The Story of Chinese chess')


class QuestionController:

    @staticmethod
    def questions_info():
        # check if current user has unfinished quiz
        quiz = Quiz.query.filter(Quiz.status == 0, Quiz.user_id == current_user.id).first()
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
            quiz = Quiz.query.filter(Quiz.status == 0, Quiz.user_id == current_user.id).first()
            if not quiz:
                quiz = Quiz(user_id=current_user.id,
                            start_question_time=datetime.now(),
                            status=0,
                            last_question_edit_time=datetime.now())
                selected_questions = Quiz.add_new_quiz(quiz, questions_in_db)

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


# controller for general view
class GeneralController:

    @staticmethod
    def general_view():
        user_count = User.get_user_count()
        tutorial_count = Tutorial.get_tutorial_count()
        question_count = Question.get_question_count()
        tutorial_average_time = Tutorial.query_tutorial_average_time()
        proportions = Quiz.get_quiz_score_distribution()
        return render_template('general.html', title='general view', user_count=user_count,
                               tutorial_count=tutorial_count, question_count=question_count,
                               tutorial_average_time=tutorial_average_time, proportions=proportions)


# controller for user view
class UserViewController:

    @staticmethod
    def user_view():
        current_tutorial = Tutorial.query_tutorial(current_user.id)
        quizzes = Quiz.get_user_quiz(current_user.id)
        return render_template('user.html', title='user view', current_tutorial=current_tutorial, quizzes=quizzes)

    @staticmethod
    def selected_quiz(quiz_id):
        quiz = Quiz.query.get(quiz_id)
        selected_questions = QuestionLog.get_selected_questions_by_quiz(quiz_id)

        return render_template('quiz-feedback.html', title='feedback', selected_questions=selected_questions,
                               quiz=quiz)
