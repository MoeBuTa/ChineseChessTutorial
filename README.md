# Chinese Chess Tutorial
A flask app for user to learn how to play Chinese Chess.

## 1. design and development



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
   
2. selenium test
Chrome version: 88.0.4324.96
OS: win10  
`python -m tests.system_tests`
