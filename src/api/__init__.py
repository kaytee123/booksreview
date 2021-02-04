from flask import Flask, Blueprint, request, jsonify
from pymongo import MongoClient


from .book import BookService


# # Setting up App
api = Blueprint('api', __name__, url_prefix="/api")

# Database Setup
uri = 'mongodb://localhost:27017/bookReview'
mongo = client = MongoClient(uri)

mongo.drop_database("bookReview")

# App Context
context = {"database": mongo.db}


@api.route('/')
def index():
    return '<h1> Book Review API </h1>'


@api.route('/v1', methods=['POST'])
def handler():
    commands = request.get_json()

    if len(commands) < 1:
        return "Error: Invalid Syntax"

    result = {}
    for cmd in commands:
        if cmd['name'] == 'AddBook':
            data = cmd['data']
            result = {cmd['name']: BookService.add_book(data, context)}

    return jsonify(result)
