# import os
#
# import posts as posts
#
# from . import db
# from flask import Flask, render_template

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# __name__ : predefined variable in python, which is set to the name of the module in which it is used
#  flask can use it as a starting point of loading associated resources such as template files
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models


if __name__ == '__main__':
    app.run(debug=True)


# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
#     )
#
#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)
#
#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
#
#     # a simple page that says hello
#     @app.route("/")
#     @app.route("/home")
#     def home():
#         return render_template('index.html', posts=posts, title='XiangQi / Chinese Chess')
#
#
#     db.init_app(app)
#     from . import auth
#     app.register_blueprint(auth.bp)
#     return app
