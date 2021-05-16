# Chinese Chess Tutorial
A flask app for user to learn how to play Chinese Chess.

## 1. design and development of the application

- a page for user registration and login
- tutorial, quiz and user view only provided for authenticated user
- tutorial part can save current reading progress for each user
- each quiz are 5 questions randomly picked from database, and can save progress and each selected answer when current user didn't finish it
- feedbacks are available for users when they finished their quizzes
- general view can see statistics: current number of user, current number of tutorial sections, current number of questions in database, an area chart for showing average reading time for each tutorial section of all users, a pie chart for showing quiz score proportion distribution for all users
- user view can see the user's tutorial progress and quiz history which shows every quizzes done by the user and can link to the corresponding feedback page. 

## 2. installing:
- Install python3.7 sqlite3
  <br>
- update pip:
`python -m pip install --upgrade pip`
  <br>
- set up a virtual environment:
`pip install virtualenv`
`virtualenv venv`

## 3.  Get Started:
- Activate the python virtual environment:
`source venv/bin/activate`
  <br>
- Install requirements.txt
`pip install -r requirements.txt`
  <br>
- build the database:
  - `flask db init` 
  - `flask db migrate`
  - `flask db upgrade`   
<br>

- To run the app:`$flask run`
- To stop the app: `$^C`
- To exit the environment:`$deactivate`


## 4. Running on the tests
1. unit test
`python -m tests.unit_tests`
   
2. selenium test:<br>
download a chromedriver (must be same as your chrome version) and put it in the tests folder <br>
`python -m tests.system_tests`
