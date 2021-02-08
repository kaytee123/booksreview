from flask import Flask, Blueprint, request, jsonify
from pymongo import MongoClient
import dns


import config
from ..shared.result import Result
from ..shared.command import CommandRunner

from . import book


# # Setting up App
api = Blueprint("api", __name__, url_prefix="/api")

# Database Setup
# Use config.MONGO_URL_LOCAL for local db
mongo = client = MongoClient(config.MONGO_URL)

# App Context
context = {"database": mongo.db}

# Command Runner Setup
command_runner = CommandRunner()
command_runner.register(book.load_commands())


@api.route("/")
def index():
    return "<h1> Book Review API </h1>"


@api.route("/v1", methods=["POST"])
def handler():
    commands = request.get_json()
    result = command_runner.execute_multiple(commands, context)
    return jsonify(result)
