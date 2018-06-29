# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, post_load

import grpc_book_service.grpc_protos.app_pb2

Publication = grpc_book_service.grpc_protos.app_pb2.Publication
Book = grpc_book_service.grpc_protos.app_pb2.Book
QueryBooksRequest = grpc_book_service.grpc_protos.app_pb2.QueryBooksRequest
GetBookRequest = grpc_book_service.grpc_protos.app_pb2.GetBookRequest


class PublicationSchema(Schema):
    name = fields.String()
    email = fields.String()

    @post_load
    def make_publication(self, data):
        return Publication(**data)


class BookSchema(Schema):
    isbn = fields.Integer()
    name = fields.String()
    author = fields.String()
    title = fields.String()
    book_type = fields.Integer()
    codes = fields.List(fields.Float())
    metadata_ref = fields.String()
    publication = fields.Nested('PublicationSchema')

    @post_load
    def make_book(self, data):
        return Book(**data)


class QueryBooksRequestSchema(Schema):
    author_prefix = fields.Integer()

    @post_load
    def make_query_books_request(self, data):
        return QueryBooksRequest(**data)


class GetBookRequestSchema(Schema):
    isbn = fields.Integer()

    @post_load
    def make_get_book_request(self, data):
        return GetBookRequest(**data)
