import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.username = 'postgres'
        self.password = 'abcd'
        self.url = '127.0.0.1:5432'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.username, self.password, self.url, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    
    Write at least one test for each test for successful operation and for expected errors.
    """
    #For Questions related routes
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_paginated_questions_errors(self):    
        res = self.client().get('/questions')
        self.route_error_500(res)

    def test_delete_questions_id(self):
        res = self.client().delete('/questions/33')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_questions_id_errors(self):   
        res = self.client().delete('/questions/97')
        self.route_error_404(res)
        self.route_error_500(res)

    def test_get_add_questions(self):
        question = {
            'question': 'Test question?',
            'answer': 'Test answer.',
            'category': '1',
            'difficulty': '2'
        }
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_get_add_questions_errors(self):  
        question = {
            'question': '',
            'answer': 'Test answer.',
            'category': '1',
            'difficulty': '2'
        }  
        res = self.client().post('/questions', json=question)
        self.route_error_422(res)
        question = {
            'question': 'Test question?',
            'answer': '',
            'category': '1',
            'difficulty': '2'
        }  
        res = self.client().post('/questions', json=question)
        self.route_error_422(res)
        self.route_error_500(res)

    def test_search_questions(self):
        keyword = {
            'searchTerm': 'this'
        }
        res = self.client().post('/question', json=keyword)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_questions_errors(self):   
        keyword = {
            'searchTerm': 'afjnjefbvkjsbdvkb'
        } 
        res = self.client().post('/question', json=keyword)

        self.route_error_404(res)
        self.route_error_500(res)       

    #For Category related routes


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_categories_errors(self):    
        res = self.client().get('/categories')

        self.route_error_500(res)
        self.route_error_404(res)

    def test_get_categories_based_questions(self):
        id = '2'
        res = self.client().get('/categories/'+id+'/questions')
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_categories_based_questions_errors(self):   
        id = '25' 
        res = self.client().get('/categories/'+id+'/questions')
        self.route_error_404(res)
        self.route_error_500(res)



 #For Quiz route        

    def test_get_quiz_first_ques(self):
        req = {
            'quiz_category': {
                'type': 'Science',
                 'id': '1'
                 },
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=req)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_quiz_first_ques_errors(self):  
        req = {
            'previous_questions': [], 
            'quiz_category': {
                'type': 'Not Science',
                 'id': '42'}
            }
        res = self.client().post('/quizzes', json=req)
        self.route_error_404(res)
        self.route_error_500(res)

    def test_get_quiz_next_ques(self):
        req = {
            'quiz_category': {
                'type': 'Science',
                 'id': '1'
                 },
            'previous_questions': [20, 21, 22]
        }  
        res = self.client().post('/quizzes',json=req)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_quiz_next_ques_errors(self):  
        req = {
            'quiz_category': {
                'type': 'Not Science',
                 'id': 'Science'
                 },
            'previous_questions': [20, 21, 22]
        }    
        res = self.client().post('/quizzes', json=req)
        self.route_error_404(res)
        self.route_error_500(res)   
    
    #Common function for Route Errors
    
    def route_error_400(self, res):
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def route_error_404(self, res):
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def route_error_422(self, res): 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')     

    def route_error_500(self, res):
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Server Error')   

              

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()