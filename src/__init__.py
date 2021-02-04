from flask import Flask, request

from .api import api
from .view import view


# Setting up App
def setup():
    app = Flask(__name__)

    # Blueprints
    app.register_blueprint(api)
    app.register_blueprint(view)

    return app
