import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # a cryptographic key, useful to generate signatures or tokens
    # to protect web forms against a nasty attack called Cross-Site Request Forgery or CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Flask-SQLAlchemy extension takes the location of the application's database from
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    # disable a feature of Flask-SQLAlchemy that
    # signal the application every time a change is about to be made in the database.
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    ENV = 'testing'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tests/test.db')

    # in memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'