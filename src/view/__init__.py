from flask import Blueprint, render_template, request, redirect, url_for

from ..api.book import BookService
from ..api import context

view = Blueprint("view", __name__, url_prefix="/")

# Home
@view.route("/")
def index():
    query = {"title": "", "sort": "title", "order": 1, "skip": 1, "take": 0}
    books = BookService.find_books(query, context)
    books = books.is_ok() if books.is_err() is False else []
    return render_template("viewbooks.html", books=books)


#  Find Single Book
@view.route("/<book_id>")
def view_reviews(book_id=None):
    query = {"id": book_id}
    book = BookService.find_book(query, context)
    book = book.is_ok() if book.is_err() is False else []
    return render_template("viewreviews.html", book=book)


# Add Book
@view.route("/addbook", methods=["POST", "GET"])
def add_book():
    new_book = {}
    error = {}
    genre = [{"genre_name", "Educative"}]

    if request.method == "POST":
        form_data = request.form.to_dict()
        new_book = BookService.add_book(form_data, context)

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
@view.route("/editbook/<book_id>", methods=["GET", "POST"])
def edit_book(book_id=None):
    error = ""
    query = {"id": book_id}
    book = BookService.find_book(query, context)

    # If Book not found or error
    if book.is_err() is False:
        book = book.is_ok()
    else:
        return redirect(url_for(".index"))

    # Handling Edit
    if request.method == "POST":
        form_data = {"id": book_id, "update": request.form.to_dict()}
        edited_book = BookService.edit_book(form_data, context)

        # Checking for error
        if edited_book.is_err():
            error = edited_book.is_err().to_dict()["message"]
            return render_template("editbook.html", book=book, error=error)

        # Book Edited
        return redirect(url_for(".index"))

    # On GET
    return render_template("editbook.html", book=book, error=error)


# Delete Book
@view.route("/delete_book/<book_id>", methods=["GET"])
def delete_book(book_id=None):
    error = ""
    query = {"id": book_id}
    book = BookService.find_book(query, context)

    # If Book not found or error
    if book.is_err() is False:
        book = book.is_ok()
    else:
        return redirect(url_for(".index"))

    # Handling Delete
    deleted_book = BookService.remove_book(query, context)

    # Checking for error
    if deleted_book.is_err():
        error = deleted_book.is_err().to_dict()["message"]
        return render_template("editbook.html", book=book, error=error)

    # Book Deleted
    return redirect(url_for(".index"))


#  Add Review
@view.route("/add_review/<book_id>", methods=["GET", "POST"])
def add_review(book_id: None):
    error = ""
    book = BookService.find_book({"id": book_id}, context)

    # If Book not found or error
    book = book.is_ok() if book.is_err() is False else {}

    if request.method == "POST":
        form_data = {"id": book_id, "review": request.form.to_dict()}
        added_review = BookService.review_book(form_data, context)

        # Checking for error
        if added_review.is_err():
            error = added_review.is_err().to_dict()
            return render_template("addreview.html", book=book, error=error)

        # Book Edited
        return redirect(url_for(".index"))

    # On GET
    return render_template("addreview.html", book=book, error=error)
