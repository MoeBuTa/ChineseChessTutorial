import random, mock
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc, func
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # write password hashes to improve security
    register_time = db.Column(db.DateTime)

    def __repr__(self):  # tells Python how to print objects of this class for debugging.
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # the id that Flask-Login passes to the function as an argument is going to be a string,
    # so databases that use numeric IDs need to convert the string to integer
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutorial_num = db.Column(db.Integer)
    title = db.Column(db.String(140))
    subtitle = db.Column(db.String(140))
    main_content = db.Column(db.UnicodeText())
    extra_content = db.Column(db.UnicodeText())
    img_url = db.Column(db.String(140))
    question_title = db.Column(db.String(140))
    answer = db.Column(db.SmallInteger())
    hint = db.Column(db.String(140))

    def __repr__(self):
        return '<Tutorial id: {}, title: {}>'.format(self.id, self.title)

    @staticmethod
    def get_tutorial_count():
        return db.session.query(func.count(Tutorial.id)).scalar()

    @classmethod
    def query_tutorial(cls, user_id):
        return cls.query.join(TutorialProgress, (TutorialProgress.read_tutorial_num == cls.tutorial_num)).filter(
            TutorialProgress.user_id == user_id).order_by(desc(TutorialProgress.last_tutorial_read_time)).first()

    @classmethod
    def query_by_num(cls, num):
        return cls.query.filter_by(tutorial_num=num).first()


class TutorialProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_duration = db.Column(db.Float(precision=10, decimal_return_scale=2))
    read_tutorial_num = db.Column(db.Integer, db.ForeignKey('tutorial.tutorial_num'))
    last_tutorial_read_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<TutorialDuration id: {}, time_duration: {}>'.format(self.id, self.time_duration)

    # query tutorial progress
    @classmethod
    def query_tutorial_progress(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(desc(cls.last_tutorial_read_time)).first()

    @classmethod
    def query_tutorial_progress_by_tutorial_num(cls, user_id, tutorial_num):
        return cls.query.filter(TutorialProgress.user_id == user_id,
                                TutorialProgress.read_tutorial_num == tutorial_num).order_by(
            desc(cls.last_tutorial_read_time)).first()

    # update tutorial progress
    @classmethod
    def save_tutorial_progress(cls, user_id, tutorial_num):

        # query last time of the tutorial progress.
        last_tutorial_progress = cls.query_tutorial_progress(user_id)

        # for new user who never read any of the tutorials
        if not last_tutorial_progress:
            current_tutorial_progress = TutorialProgress(user_id=user_id,
                                                         read_tutorial_num=tutorial_num)
            db.session.add(current_tutorial_progress)
        else:
            # update time_duration and read_time
            time_duration = (datetime.now() - last_tutorial_progress.last_tutorial_read_time).seconds / 60
            if time_duration < 5:
                last_tutorial_progress.time_duration = time_duration
            else:
                last_tutorial_progress.time_duration = 5
            last_tutorial_progress.last_tutorial_read_time = datetime.now()

            # query if the user read the current tutorial
            current_tutorial_progress = cls.query_tutorial_progress_by_tutorial_num(user_id, tutorial_num)
            if not current_tutorial_progress:
                # add new tutorial progress
                current_tutorial_progress = TutorialProgress(user_id=user_id, time_duration=0,
                                                             read_tutorial_num=tutorial_num,
                                                             last_tutorial_read_time=datetime.now())
                db.session.add(current_tutorial_progress)
            else:
                # update tutorial progress
                current_tutorial_progress.last_tutorial_read_time = datetime.now()
        db.session.commit()

    def set_first_read_time(self):
        self.last_tutorial_read_time = datetime.now()
        db.session.commit()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    option_one = db.Column(db.String(40))
    option_two = db.Column(db.String(40))
    option_three = db.Column(db.String(40))
    option_four = db.Column(db.String(40))

    def __repr__(self):
        return '<Question body: {}>'.format(self.body)

    @classmethod
    def get_selected_question(cls, id):
        return cls.query.join(
            QuestionLog, (Question.id == QuestionLog.question_id)).filter(
            QuestionLog.quiz_id == id).order_by(
            asc(QuestionLog.current_question_num)
        ).add_entity(QuestionLog).all()


class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer = db.Column(db.String(40))
    score = db.Column(db.Float(precision=10, decimal_return_scale=2))

    def __repr__(self):
        return '<QuestionAnswer question_id: {}, answer: {}>'.format(self.question_id, self.answer)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_score = db.Column(db.Float(precision=10, decimal_return_scale=2))
    feedback = db.Column(db.UnicodeText())
    start_question_time = db.Column(db.DateTime)
    last_question_edit_time = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Quiz status: {}, total_score:{}, user_id:{}>'.format(self.status, self.total_score, self.user_id)

    @staticmethod
    def addNewQuiz(quiz, questions):
        selected_questions = []
        db.session.add(quiz)
        db.session.flush()
        quiz_id = quiz.id

        # select questions randomly
        j = 0
        for i in random.sample(range(1, len(questions)), 5):
            j += 1
            quest = QuestionLog(question_id=questions[i].id,
                                current_question_num=j, quiz_id=quiz_id)
            selected_quest = mock.Mock()
            selected_quest.Question = questions[i]
            selected_quest.QuestionLog = quest

            selected_questions.append(selected_quest)
            db.session.add(quest)
        db.session.commit()
        return selected_questions

    def update_quiz_edit_time(self):
        self.last_question_edit_time = datetime.now()
        db.session.commit()

    def submit_quiz(self, total_score):
        self.last_question_edit_time = datetime.now()
        self.total_score = total_score
        self.status = 1
        db.session.commit()

    @staticmethod
    def get_quizzes_count():
        return db.session.query(func.count(Quiz.id)).scalar()


class QuestionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    selected_answer = db.Column(db.String(40))
    current_question_num = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    correct = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<QuestionLog selected_answer: {}, quiz_id: {}, current_question_num: {}>'.format(
            self.selected_answer, self.quiz_id, self.current_question_num)

    def save_question_progress(self, selected_answer):
        self.selected_answer = selected_answer
        db.session.commit()

    @classmethod
    def get_selected_question_answer(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).join(
            QuestionAnswer, (QuestionLog.question_id == QuestionAnswer.question_id)).join(Question, (
                QuestionLog.question_id == Question.id)).order_by(
            asc(QuestionLog.current_question_num)).add_entity(
            QuestionAnswer).add_entity(Question).all()
