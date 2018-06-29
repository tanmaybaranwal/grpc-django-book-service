from grpc_book_service.utils.not_found import NotFound


def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    isbn = request_data['isbn']

    from grpc_book_service.models import Book
    try:
        book = Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        raise NotFound("Book Not Found")

    response = {
        "isbn": book.isbn,
        "name": book.name,
        "title": book.title,
        "author": book.author.author_name,
        "book_type": book.book_type,
        "codes": [1.0, 2.5, 5.5],
        "metadata_ref": book.metadata_ref
    }
    import json
    if book.publication:
        publication = json.loads(book.publication)
        response.update({
            "publication": publication
        })

    return response
