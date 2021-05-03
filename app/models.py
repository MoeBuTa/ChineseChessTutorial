from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

tutorial_progress = db.Table('tutorial_progress',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                       db.Column('tutorial_id', db.Integer, db.ForeignKey('tutorial.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # write password hashes to improve security
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
        return '<Tutorial {}, {}>'.format(self.id, self.title)


# class Story(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # main_text = db.Column(db.UnicodeText())
