import unittest
from app import create_app, db
from tests import data
from app.models import User, Tutorial, TutorialProgress, Question, Quiz, QuestionLog
from config import TestingConfig
from datetime import datetime


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        data.add_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='moebuta')
        u.set_password('1a2b3c')
        self.assertFalse(u.check_password('12345'))
        self.assertTrue(u.check_password('1a2b3c'))

    def test_register(self):
        user1 = User(username='John', email='12345@gmail.com', register_time=datetime.now())
        message1 = user1.register_validation("12345")
        self.assertEqual(message1, 'Please use a different username!')
        user2 = User(username='Daniel', email='12345@gmail.com', register_time=datetime.now())
        message2 = user2.register_validation("12345")
        self.assertEqual(message2, 'Please use a different email address!')
        user3 = User(username='RandomGuy', email='123456@gmail.com', register_time=datetime.now())
        message3 = user3.register_validation("12345")
        self.assertEqual(message3, 'success')

    def test_query_tutorial_by_num(self):
        tutorial = Tutorial.query_by_num(3)
        self.assertEqual(tutorial.tutorial_num, 3)

    def test_tutorial_count(self):
        count = Tutorial.get_tutorial_count()
        self.assertEqual(count, 8)

    def test_tutorial_progress(self):
        # add new user template
        user = User(username='RandomGuy', email='1234567@gmail.com', register_time=datetime.now())
        user.register_validation("12345")
        progress = TutorialProgress.query_tutorial_progress(user.id)
        self.assertEqual(progress.user_id, user.id)

    def test_add_quiz_and_select_questions(self):
        # add quiz and log
        questions_in_db = Question.query.all()
        quiz = Quiz(user_id=1,
                    start_question_time=datetime.now(),
                    status=0,
                    last_question_edit_time=datetime.now())
        selected_questions = Quiz.add_new_quiz(quiz, questions_in_db)
        self.assertEqual(selected_questions[0].QuestionLog.quiz_id, quiz.id)

    def test_save_question_progress(self):
        # add quiz and log
        questions_in_db = Question.query.all()
        quiz = Quiz(user_id=1,
                    start_question_time=datetime.now(),
                    status=0,
                    last_question_edit_time=datetime.now())
        Quiz.add_new_quiz(quiz, questions_in_db)

        # save progress
        question_log = QuestionLog.query.get(1)
        question_log.save_question_progress("abc")

        self.assertEqual(question_log.selected_answer, "abc")

    def test_update_quiz_edit_time(self):
        # add quiz and log
        questions_in_db = Question.query.all()
        quiz = Quiz(user_id=1,
                    start_question_time=datetime.now(),
                    status=0,
                    last_question_edit_time=datetime.now())
        Quiz.add_new_quiz(quiz, questions_in_db)

        # update quiz edit time
        edit_time = quiz.update_quiz_edit_time()
        self.assertEqual(quiz.last_question_edit_time, edit_time)


if __name__ == '__main__':
    unittest.main(verbosity=2)
