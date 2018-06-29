def api_wrapper(*args, **kwargs):
    request_data = kwargs['request_data']
    author_prefix = request_data['author_prefix']
    from grpc_book_service.models import Book
    books = Book.objects.filter(author__author_name__istartswith=author_prefix)
    if books:
        book = books[0]
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
    return {}
