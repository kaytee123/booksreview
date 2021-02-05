from bson.objectid import ObjectId
from ..shared.command import Command
from ..shared.filter import Filter
from ..shared.result import Result, Error


class Book:
    def __init__(self, id, title, author, cover_image_link, purchase_link, genre, summary, created_at, reviews):
        self.id = id
        self.title = title
        self.author = author
        self.cover_image_link = cover_image_link
        self.purchase_link = purchase_link
        self.genre = genre
        self.summary = summary
        self.created_at = created_at
        self.reviews = reviews

    @staticmethod
    def create(book):
        validity = Book.validate(book)

        if validity['valid'] is False:
            return Result.err(Error(
                validity['message'],
                'USERINPUT',
                validity['errors']
            ))

        return Result.ok(Book(
            id=str(ObjectId(book.get('id'))),
            title=book.get('title'),
            author=book.get('author'),
            cover_image_link=book.get('coverImageLink'),
            purchase_link=book.get('purchaseLink'),
            genre=book.get('genre'),
            summary=book.get('summary'),
            created_at=book.get('createdAt'),
            reviews=book.get('reviews', [])
        ))

    @ staticmethod
    def validate(book):
        errors = {}

        if not book.get('title') or book.get('title') == '':
            errors['title'] = 'Title is required'

        if not book.get('author') or book.get('author') == '':
            errors['author'] = 'Author is required'

        if not book.get('coverImageLink') or book.get('coverImageLink') == '':
            errors['coverImageLink'] = 'Cover is required'

        if not book.get('purchaseLink') or book.get('purchaseLink') == '':
            errors['purchaseLink'] = 'Purchase Link is required'

        if not book.get('genre') or book.get('genre') == '':
            errors['genre'] = 'Genre is required'

        if not book.get('summary') or book.get('summary') == '':
            errors['summary'] = 'Summary is required'

        message = ''
        for key in errors:
            message += errors[key] + '. '

        return {
            'valid': True if len(errors) == 0 else False,
            'errors': errors,
            'message': message
        }


class BookMapper:
    @staticmethod
    def to_domain(raw_book):
        return Book(
            id=str(raw_book.get('_id', None)),
            title=raw_book.get('title', None),
            author=raw_book.get('author', None),
            cover_image_link=raw_book.get('coverImageLink', None),
            purchase_link=raw_book.get('purchaseLink', None),
            genre=raw_book.get('genre', None),
            summary=raw_book.get('summary', None),
            created_at=raw_book.get('createdAt', None),
            reviews=raw_book.get('reviews', None)
        )

    @staticmethod
    def to_dict(book: Book, id_shape='id'):
        return {
            id_shape: book.id,
            'title': book.title,
            'author': book.author,
            'coverImageLink': book.cover_image_link,
            'purchaseLink': book.purchase_link,
            'genre': book.genre,
            'summary': book.summary,
            'createdAt': book.created_at,
            'reviews': book.reviews
        }

    @staticmethod
    def for_update(data: dict):
        update = {}

        if data['title']:
            update['title'] = data['title']
        if data['author']:
            update['author'] = data['author']
        # if data['coverImageLink']:
        #     update['coverImageLink'] = data['coverImageLink']
        # if data['purchaseLink']:
        #     update['purchaseLink'] = data['purchaseLink']
        if data['genre']:
            update['genre'] = data['genre']
        # if data['summary']:
        #     update['summary'] = data['summary']
        return update

    @staticmethod
    def to_persistence(book: Book):
        return BookMapper.to_dict(book, id_shape='_id')


class BookRepo:

    @ staticmethod
    def add(book: Book, db):
        books = db['bookReview']['books']
        new_book = BookMapper.to_persistence(book)
        doc_id = books.insert_one(new_book).inserted_id
        doc = books.find_one({'_id': doc_id})

        return Result.ok(BookMapper.to_domain(doc))

    @ staticmethod
    def find(query: Filter, db):
        books = db['bookReview']['books']
        qry = {'title': {"$regex": '^'+query.title}}
        docs = books.find(qry).sort(query.sort, query.order).limit(
            query.take).skip(query.skip)

        if not docs:
            return Result.err(Error(
                'Book not found',
                'NOTFOUND',
                {}
            ))

        books = [BookMapper.to_domain(doc) for doc in docs]
        return Result.ok(books)

    @ staticmethod
    def find_by_id(book_id, db):
        books = db['bookReview']['books']
        doc = books.find_one({'_id': book_id})

        if not doc:
            return Result.err(Error(
                'Book not found',
                'NOTFOUND',
                {'id': book_id}
            ))

        book = BookMapper.to_domain(doc)
        return Result.ok(book)

    @ staticmethod
    def update(book_id: str, update: dict, db):
        books = db['bookReview']['books']
        book_update = BookMapper.for_update(update)
        book_update = {'$set': book_update}

        books.update_one({'_id': book_id}, book_update)
        doc = books.find_one({'_id': book_id})

        return Result.ok(BookMapper.to_domain(doc))

    @ staticmethod
    def remove(book_id, db):
        books = db['bookReview']['books']

        try:
            doc = books.find_one({'_id': book_id})
            if not doc:
                return Result.err(Error(
                    'Book not found',
                    'NOTFOUND',
                    {'id': book_id}
                ))

            # Deleting
            books.delete_one({'_id': book_id})

            book = BookMapper.to_domain(doc)
            return Result.ok(book)
        except Exception as e:
            return Result.err(Error(
                'Error occured while removing book',
                'TECHNICAL',
                {'id': book_id, 'e': e}
            ))


# Commands
class AddBook(Command):
    @staticmethod
    def name():
        return 'AddBook'

    @staticmethod
    def handle(data, context):
        book_or_err = Book.create(data)

        if book_or_err.is_err():
            return book_or_err

        saved_or_err = BookRepo.add(
            book_or_err.is_ok(),
            context.get('database')
        ).match(
            lambda book: Result.ok(BookMapper.to_dict(book)),
            lambda err: Result.err(err)
        )

        return saved_or_err


class FindBook(Command):
    @staticmethod
    def name():
        return 'FindBook'

    @staticmethod
    def handle(data, context):

        if not data.get('id', None):
            return Result.err(Error('Book id is requires', 'USERINPUT'))

        book_or_err = BookRepo.find_by_id(
            data['id'],
            context.get('database', None)
        )

        result = book_or_err.match(
            lambda book: Result.ok(BookMapper.to_dict(book)),
            lambda err: Result.err(err)
        )

        return result


class FindBooks(Command):
    @staticmethod
    def name():
        return 'FindBooks'

    @staticmethod
    def handle(data: dict, context: dict):

        books_or_err = BookRepo.find(
            Filter.create(data),
            context.get('database', None)
        )

        def to_dict(books): return [BookMapper.to_dict(book) for book in books]

        result = books_or_err.match(
            lambda books: Result.ok(to_dict(books)),
            lambda err: Result.err(err)
        )

        return result


class EditBook(Command):
    @staticmethod
    def name():
        return 'EditBook'

    @staticmethod
    def handle(data, context):

        # Checking Parameters
        if not data.get('id', None):
            return Result.err(Error('Book id is requires', 'USERINPUT'))

        if not data.get('update', None):
            return Result.err(Error('Book update is requires', 'USERINPUT'))

        # Validate Update
        # update_or_err = Book.validate_update(data['update'])

        # if update_or_err.is_err():
        #     return update_or_err

        # Updating
        book_or_err = BookRepo.update(
            data['id'],
            data['update'],
            context.get('database', None)
        )

        result = book_or_err.match(
            lambda book: Result.ok(BookMapper.to_dict(book)),
            lambda err: Result.err(err)
        )

        return result


class RemoveBook(Command):
    @staticmethod
    def name():
        return 'RemoveBook'

    @staticmethod
    def handle(data, context):

        if not data.get('id', None):
            return Result.err(Error('Book id is requires', 'USERINPUT'))

        deleted_or_err = BookRepo.remove(
            data['id'],
            context.get('database', None)
        )

        result = deleted_or_err.match(
            lambda book: Result.ok(BookMapper.to_dict(book)),
            lambda err: Result.err(err)
        )

        return result


class ReviewBook(Command):
    @staticmethod
    def name():
        return 'ReviewBook'

    @staticmethod
    def handle(data, context):
        pass


commands = [AddBook, FindBook, FindBooks, EditBook, RemoveBook]


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
