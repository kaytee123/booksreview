from bson.objectid import ObjectId
from ..shared.command import Command


class Book:
    def __init__(self, id, title, author, cover_image_link, purchase_link, genre, summary, created_at):
        self.id = id
        self.title = title
        self.cover_image_link = cover_image_link
        self.purchase_link = purchase_link
        self.genre = genre
        self.summary = summary
        self.created_at = created_at

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def create(book):
        validity = Book.validate(book)

        if validity.get('valid') is False:
            return validity

        return Book(
            id=str(ObjectId(book.get('id'))),
            title=book.get('title'),
            author=book.get('author'),
            cover_image_link=book.get('coverImageLink'),
            purchase_link=book.get('purchaseLink'),
            genre=book.get('genre'),
            summary=book.get('summary'),
            created_at=book.get('createdAt')
        )

    @ staticmethod
    def validate(book):
        errors = []

        if book.get('title') is not str or book.get('title') == '':
            errors.append({'title': 'Title is required'})

        if book.get('author') is not str or book.get('author') == '':
            errors.append({'author': 'Author is required'})

        if book.get('coverImageLink') is not str or book.get('coverImageLink') == '':
            errors.append({'coverImageLink': 'Cover is required'})

        if book.get('purchaseLink') is not str or book.get('purchaseLink') == '':
            errors.append({'purchaseLink': 'Purchase Link is required'})

        if book.get('genre') is not str or book.get('genre') == '':
            errors.append({'genre': 'Genre is required'})

        if book.get('summary') is not str or book.get('summary') == '':
            errors.append({'summary': 'Summary is required'})

        return {
            'valid': True if len(errors) else False,
            'errors': errors
        }


class BookMapper:
    @ staticmethod
    def to_domain(raw_book):
        return Book(
            id=str(raw_book.get('_id')),
            title=raw_book.get('title'),
            author=raw_book.get('author'),
            cover_image_link=raw_book.get('coverImageLink'),
            purchase_link=raw_book.get('purchaseLink'),
            genre=raw_book.get('genre'),
            summary=raw_book.get('summary'),
            created_at=raw_book.get('createdAt')
        )

    @ staticmethod
    def to_dict(book: Book, id_shape='id'):
        return {
            id_shape: book.id,
            'title': book.title
        }

    @ staticmethod
    def to_persistence(book: Book):
        return BookMapper.to_dict(book, id_shape='_id')


class BookRepo:

    @ staticmethod
    def add(book: Book, db):
        books = db['bookReview']['books']
        new_book = BookMapper.to_persistence(book)
        doc_id = books.insert_one(new_book).inserted_id
        doc = books.find_one({'_id': doc_id})

        return BookMapper.to_domain(doc)

    @ staticmethod
    def find(query, db):
        books = db['bookReview']['books']
        docs = books.find()
        result = [BookMapper.to_domain(doc) for doc in docs]

        return result

    @ staticmethod
    def find_by_id(id, db):
        books = db['bookReview']['books']
        doc = books.find_book({'_id': id})
        book = BookMapper.to_domain(doc)

        return book


# Commands
class AddBook(Command):
    @staticmethod
    def name():
        return 'AddBook'

    @staticmethod
    def handle(data, context):
        book = Book.create(data)

        saved_book = BookRepo.add(book, context.get('database'))
        # return BookMapper.to_dict(book)
        return saved_book.to_dict()


class FindBook(Command):
    @staticmethod
    def name():
        return 'FindBook'

    @staticmethod
    def handle(data, context):
        book = BookRepo.find_by_id(data.get('id'), context.get('database'))
        return BookMapper.to_dict(book)


class FindBooks(Command):
    @staticmethod
    def name():
        return 'AddBooks'

    @staticmethod
    def handle(data: dict, context: dict):
        books = BookRepo.find(data, context.get('database'))
        result = [BookMapper.to_dict(book) for book in books]

        return result


class EditBook(Command):
    @staticmethod
    def name():
        return 'EditBook'

    @staticmethod
    def handle(data, context):
        """ Unimplemented """
        pass


class RemoveBook(Command):
    @staticmethod
    def name():
        return 'RemoveBook'

    @staticmethod
    def handle(data, context):
        """ Unimplemented """
        pass


class ReviewBook(Command):
    @staticmethod
    def name():
        return 'ReviewBook'

    @staticmethod
    def handle(data, context):
        """ Unimplemented """
        pass


# Service
class BookService:
    @ staticmethod
    def add_book(data, context):
        return AddBook.handle(data, context)

    @ staticmethod
    def find_book(query, context):
        return FindBook.handle(query, context)

    @ staticmethod
    def find_books(query, context):
        return FindBooks.handle(query, context)

    @ staticmethod
    def edit_book(query, context):
        pass

    @ staticmethod
    def remove_book(query, context):
        pass

    @ staticmethod
    def review_book(query, context):
        pass
