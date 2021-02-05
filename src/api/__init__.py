from flask import Flask, Blueprint, request, jsonify
from pymongo import MongoClient


from ..shared.result import Result
from ..shared.command import CommandRunner


from . import book


# # Setting up App
api = Blueprint('api', __name__, url_prefix="/api")

# Database Setup
uri = 'mongodb://localhost:27017/bookReview'
mongo = client = MongoClient(uri)

# mongo.drop_database("bookReview")

# App Context
context = {"database": mongo.db}

# Command Runner Setup
command_runner = CommandRunner()
command_runner.register(book.commands)


@api.route('/')
def index():
    return '<h1> Book Review API </h1>'


@api.route('/v1', methods=['POST'])
def handler():
    commands = request.get_json()
    result = command_runner.execute_multiple(commands, context)
    return jsonify(result)
