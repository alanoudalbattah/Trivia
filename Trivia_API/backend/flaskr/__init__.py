import os
from flask import (
  Flask, render_template, abort,
  request, redirect, jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  ✅@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  ✅@TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  #? Access-Control-Allow-Origin: What client domains can access its resources. For any domain use *
  #? Access-Control-Allow-Credentials: Only if using cookies for authentication - in which case its value must be true
  #? Access-Control-Allow-Methods: List of HTTP request types allowed
  #? Access-Control-Allow-Headers: List of http request header values the server will allow, particularly useful if you use any custom headers
  @app.after_request
  def after_request(res):
      res.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return res
  '''
  ✅@TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def categories():
    
    formatted_categories = [category.format() for category in Category.query.all()]
    
    return jsonify({
      'success': True,
      'categories':formatted_categories
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def questions():
    #* Implement pagniation
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    formatted_questions = [question.format() for question in Question.query.all()]

    return jsonify({
      'success': True,
      'questions':formatted_questions[start:end],
      'totalQuestions': len(formatted_questions),
      'categories': [category.type for category in Category.query.all()],
     #! 'currentCategory': ques
      })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  ✅@TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  #? indicates that the server cannot or will not process the request
  #? due to something that is perceived to be a client error 
  def bad_request(error):
      return jsonify({
          "success": False, 
          "error": 400,
          "message": "Bad request"
          }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "Not found"
          }), 404

  @app.errorhandler(405)
  #? indicates that the request method is known by the server but is
  #? not supported by the target resource.
  def method_not_allowed(error):
      return jsonify({
          "success": False, 
          "error": 405,
          "message": "Method not allowed"
          }), 405

  @app.errorhandler(422)
  #? indicates that the server understands the content type of the request
  #? entity, and the syntax of the request entity is correct, but it was
  #? unable to process the contained instructions.
  def unprocessable_entity(error):
      return jsonify({
          "success": False, 
          "error": 422,
          "message": "Unprocessable entity"
          }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False, 
          "error": 500,
          "message": "Internal server error"
          }), 500
#* Status Code Source: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
  return app

    