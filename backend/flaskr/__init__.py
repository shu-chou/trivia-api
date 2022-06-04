from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  try:
   setup_db(app)
  except:
     abort(500) 
  
  '''
  Cors to Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  
  '''
  after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''
  
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories(): 
    try:
      rows = Category.query.all()
    except:
      abort(500) 
    if rows is None:
      abort(404)  
    dict = {}
    for category in rows:
        dict[str(category.id)] = category.type
    return jsonify({
      'success': True,
      'categories': dict
    })
 

  '''
  
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.
  ''' 
  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    try:
      rows = Question.query.all()
      questions = [row.format() for row in rows]
      categories = Category.query.all()
      dict = {}
      for category in categories:
          dict[str(category.id)] = category.type
      return jsonify({
        'success': True,
        'questions': questions[start:end], 
        'total_questions': len(questions),
        'categories': dict,
        'current_category': None
      })
    except:
      abort(500)  

  ''' 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<id>', methods=['DELETE'])
  def del_ques(id):
    ques = Question.query.get(int(id))
    if ques is None:
       abort(404)
    try:   
      ques.delete()
      return jsonify({
        'success': True
      })
    except:
      abort(500)  
  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
   
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def post_quizz():
    req = request.get_json()
    if not(req['question'] and req['question'].strip()):
       abort(422)
    if not(req['answer'] and req['answer'].strip()):
       abort(422)
    new_ques = Question(
    question=req['question'], 
    answer=req['answer'], 
    difficulty =req['difficulty'], 
    category=req['category']
    )  
    try:
      new_ques.insert()
      return jsonify({
      'success': True
    })
    except:
        abort(500)
  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
   
  '''
  
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/question', methods=['POST'])
  def find_ques():
    req = request.get_json()
    try:
      results = Question.findQues(str(req['searchTerm']))
    except:
        abort(500)   
    if len(results)==0:
         abort(404)
    questions =[result.format() for result in results]
    return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        'current_category': 'None'
      })
 
  '''
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  
  Create a GET endpoint to get questions based on category. 
  '''
  @app.route('/categories/<id>/questions', methods=['GET'])
  def get_category_ques(id): 
    try:
      rows = Question.query.filter(Question.category == str(id)).all()
      if rows is None:
         abort(404)
      category = Category.query.get(id)
      if category is None:
         abort(404)
      questions = [row.format() for row in rows]
      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        'current_category': str(category.type)
      })
    except:
        abort(500)  

  '''
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions.
  ''' 
  @app.route('/quizzes', methods=['POST'])
  def post_quiz():
    req = request.get_json()
    category = req['quiz_category']['id']
    prev_ques = req['previous_questions']   
    if category == 0:
      result = play_all(prev_ques)
    if category != 0:
      result = play_specific(category, prev_ques)
    return result       

  # Quiz Functions to play all questions
  # when category == 0
  # Takes ques_arr as input argument
  # Return jsonify question object 
  def play_all(ques_arr):
    if len(ques_arr) <= 0:
       try:
        question = Question.query.order_by(Question.id.asc()).first()
        if question is None:
           abort(404)
       except:
          abort(500) 
    if len(ques_arr) >= 1:
      try:
       question = Question.query.\
                  filter(Question.id.not_in(ques_arr)).\
                  order_by(Question.id.asc()).first()
      except:
        abort(500)
      if question is None:
        return jsonify({
          'success': True
        })              
    return jsonify({
      'success': True,
      'question': question.format()
    }) 

  # Quiz function to play specific questions
  # when category == 1
  # Takes category and ques_arr as input argument
  # Return jsonify question object 
  def play_specific(category, ques_arr):
    if len(ques_arr) <= 0:
       try:
        question = Question.query.filter_by(category=category).order_by(Question.id.asc()).first()
        if question is None:
           abort(404)
       except:
          abort(500) 
    if len(ques_arr) >= 1:
      try:
       question = Question.query.filter_by(category=category).\
                  filter(Question.id.not_in(ques_arr)).\
                  order_by(Question.id.asc()).first()
      except:
        abort(500)
      if question is None:
        return jsonify({
          'success': True
        })              
    return jsonify({
      'success': True,
      'question': question.format()
    })
  '''
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
      }), 400  

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server Error'
      }), 500        
  
  @app.errorhandler(422)
  def server_error(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
      }), 422   
  return app