from flask import Blueprint, render_template, request, redirect, url_for

from ..api.book import BookService
from ..api import context


view = Blueprint("view", __name__, url_prefix="/")


@view.route("/")
@view.route("/view_books")
def index():
    query = {"title": "", "sort": "title", "order": 1, "skip": 1, "take": 0}
    books = BookService.find_books(query, context)
    books = books.is_ok() if books.is_err() is False else []
    return render_template("test_temp.html", books=books)


# Add Book
@view.route("/addbook", methods=["POST", "GET"])
def add_book():
    new_book = {}
    error = {}
    genre = [{"genre_name", "Educative"}]

    if request.method == "POST":
        book_data = {
            "title": request.form["title"],
            "author": request.form["author"],
            "coverImageLink": request.form["coverImageLink"],
            "purchaseLink": request.form["purchaseLink"],
            "genre": request.form["genre"],
            "summary": request.form["summary"],
        }
        new_book = BookService.add_book(book_data, context)

        # Checking for error
        if new_book.is_err():
            print("Error Addbook")
            error = new_book.is_err().to_dict()
            return render_template("addbook.html", error=error, genre=genre)

        # Book Added
        return redirect(url_for(".index"))

    # On GET
    return render_template("addbook.html", error=error, genre=genre)


# Edit Book
@view.route(
    "/editbook",
)
def edit_book():
    book_data = {
        "title": request.form["title"],
        "author": request.form["author"],
        "coverImageLink": request.form["coverImageLink"],
        "purchaseLink": request.form["purchaseLink"],
        "genre": request.form["genre"],
        "summary": request.form["summary"],
    }
    new_book = BookService.add_book(book_data, context)

    # Checking for error
    # if new_book.is_err()
    #     error = new_book.is_err().to_dict()
    #     return render_template('editbook.html', error=error )
    return "Hey"
    return redirect("/")
