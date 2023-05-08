from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)
    # new_book = Book(title=request_body["title"],
    #                 description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)



@books_bp.route("", methods=["GET"])
def read_all_books():

    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    #     books_response.append({
    #         "id": book.id,
    #         "title": book.title,
    #         "description": book.description
    #     })

    return jsonify(books_response)



def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    book = cls.query.get(model_id)

    if not book:
        message = f"{cls.__name__} {model_id} not found"
        abort(make_response({"message": message}, 404))
        # abort(make_response({"message":f"book {model_id} not found"}, 404))
    
    return book



@books_bp.route("/<model_id>", methods=["GET"])
def read_one_book(model_id):
    # book = Book.query.get(model_id)
    book = validate_model(Book, model_id)
    return book.to_dict()
    #return jsonify(book.to_dict()), 200



@books_bp.route("/<model_id>", methods=["PUT"])
def update_book(model_id):
    book = validate_model(Book, model_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated"))




@books_bp.route("/<model_id>", methods=["DELETE"])
def delete_book(model_id):
    book = validate_model(Book, model_id)

    db.session.delete(book)
    db.session.commit()

    message = f"Book #{book} successfully deleted"
    return make_response(jsonify({"Message": message}, 200))

    # return (f"Book #{model_id} successfully deleted", 200)


# FLASK_ENV=development flask run








# def validate_book(book_id):
    # try:
    #     book_id = int(book_id)
    # except:
    #     abort(make_response({"message":f"book {book_id} invalid"}, 400))

    # for book in books:
    #     if book.id == book_id:
    #         return book_id

    # abort(make_response({"message":f"book {book_id} not found"}, 404))


# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })

#     return jsonify(books_response)

# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id)
    
#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }

        
# hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body

# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]