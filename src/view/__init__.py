
from flask import Blueprint, render_template

from ..api.book import BookService
from ..api import context


view = Blueprint('view', __name__, url_prefix="/")


@view.route('/')
def index():
    query = {
        "title": "",
        "sort": "title",
        "order": 1,
        "skip": 1,
        "take": 0
    }
    books = BookService.find_books(query, context)
    books = books.is_ok() if books.is_err() is False else []
    return render_template("test_temp.html", books=books)
