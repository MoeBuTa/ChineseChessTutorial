import random, mock
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc, func
from flask_login import UserMixin
from datetime import datetime

tutorial_progress = db.Table('tutorial_progress',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             db.Column('tutorial_id', db.Integer, db.ForeignKey('tutorial.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # write password hashes to improve security
    register_time = db.Column(db.DateTime)
    last_tutorial_read_time = db.Column(db.DateTime)

    # one-to-one: tutorial - user
    # This relationship links User instances to Tutorial instances
    # Tutorial: target entity
    # secondary: configures the association table that is used for this relationship
    # primaryjoin: the condition that links the left side entity
    # secondaryjoin: ...........................right...........
    # backref: defines how this relationship will be accessed from the right side entity
    # lazy: execution mode (dynamic sets up the query to not run until specifically requested)
    tutorial_checked = db.relationship(
        'Tutorial', secondary=tutorial_progress,
        backref='user', uselist=False)

    def __repr__(self):  # tells Python how to print objects of this class for debugging.
        return '<User {}>'.format(self.username)

    # update tutorial progress
    def save_tutorial_progress(self, tutorial_id):
        if not self.tutorial_checked:
            statement = tutorial_progress.insert().values(tutorial_id=tutorial_id, user_id=self.id)
        else:
            user = User.query.get(self.id)
            user.last_tutorial_read_time = datetime.now()
            statement = tutorial_progress.update().where(
                tutorial_progress.c.user_id == self.id).values(tutorial_id=tutorial_id)
        db.session.execute(statement)
        db.session.commit()

    # query tutorial progress
    def query_tutorial_progress(self):
        return self.tutorial_checked

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


# class Story(db.Model):
# id = db.Column(db.Integer, primary_key=True)
# main_text = db.Column(db.UnicodeText())


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    option_one = db.Column(db.String(40))
    option_two = db.Column(db.String(40))
    option_three = db.Column(db.String(40))
    option_four = db.Column(db.String(40))

    def __repr__(self):
        return '<Assessment body: {}>'.format(self.body)

    @classmethod
    def get_selected_assessment(cls, id):
        return cls.query.join(
            AssessmentLog, (Assessment.id == AssessmentLog.assessment_id)).filter(
            AssessmentLog.quiz_id == id).order_by(
            asc(AssessmentLog.current_assessment_num)
        ).add_entity(AssessmentLog).all()


class AssessmentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    answer = db.Column(db.String(40))
    score = db.Column(db.Float(precision=10, decimal_return_scale=2))

    def __repr__(self):
        return '<AssessmentAnswer assessment_id: {}, answer: {}>'.format(self.assessment_id, self.answer)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_score = db.Column(db.Float(precision=10, decimal_return_scale=2))
    feedback = db.Column(db.UnicodeText())
    start_assessment_time = db.Column(db.DateTime)
    last_assessment_edit_time = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Quiz status: {}>'.format(self.status)

    @staticmethod
    def addNewQuiz(quiz, assessments):
        selected_assessments = []
        db.session.add(quiz)
        db.session.flush()
        quiz_id = quiz.id

        # select assessments randomly
        j = 0
        for i in random.sample(range(1, len(assessments)), 5):
            j += 1
            assess = AssessmentLog(assessment_id=assessments[i].id,
                                   current_assessment_num=j, quiz_id=quiz_id)
            selected_assess = mock.Mock()
            selected_assess.Assessment = assessments[i]
            selected_assess.AssessmentLog = assess

            selected_assessments.append(selected_assess)
            db.session.add(assess)
        db.session.commit()
        return selected_assessments

    def update_quiz_edit_time(self):
        self.last_assessment_edit_time = datetime.now()
        db.session.commit()

    def submit_quiz(self, total_score):
        self.last_assessment_edit_time = datetime.now()
        self.total_score = total_score
        self.status = 1
        db.session.commit()


class AssessmentLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
    selected_answer = db.Column(db.String(40))
    current_assessment_num = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    correct = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<AssessmentLog selected_answer: {}, quiz_id: {}, current_assessment_num{}>'.format(
            self.selected_answer, self.quiz_id, self.current_assessment_num)

    def save_assessment_progress(self, selected_answer):
        self.selected_answer = selected_answer
        db.session.commit()

    @classmethod
    def get_selected_assessment_answer(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).join(
            AssessmentAnswer, (AssessmentLog.assessment_id == AssessmentAnswer.assessment_id)).join(Assessment, (
                AssessmentLog.assessment_id == Assessment.id)).order_by(
            asc(AssessmentLog.current_assessment_num)).add_entity(
            AssessmentAnswer).add_entity(Assessment).all()
