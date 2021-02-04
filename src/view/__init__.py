
from flask import Blueprint


view = Blueprint('view', __name__, url_prefix="/")


@view.route('/')
def index():
    return '<h1> Book Review </h1>'
