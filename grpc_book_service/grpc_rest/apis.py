# -*- coding: utf-8 -*-

from restart.api import RESTArt
from restart.exceptions import BadRequest, InternalServerError
from restart.parsers import JSONParser
from restart.renderers import JSONRenderer
from restart.resource import Resource

import schemas
import services

api = RESTArt()
grpc_book_service = services.GRPCBookService('localhost:50051')


class GRPCMessageParser(JSONParser):
    """Deserialize JSON to gRPC message object."""

    def parse(self, stream, content_type, content_length, context=None):
        resource = context['resource']
        data = super(GRPCMessageParser, self).parse(
            stream, content_type, content_length, context)
        deserialized = resource.req_schema.load(data)
        if deserialized.errors:
            raise BadRequest(deserialized.errors)
        return deserialized.data


class GRPCMessageRenderer(JSONRenderer):
    """Serialize gRPC message object to JSON."""

    def render(self, data, context=None):
        resource = context['resource']
        serialized = resource.resp_schema.dump(data)
        if serialized.errors:
            raise InternalServerError(serialized.errors)
        return super(GRPCMessageRenderer, self).render(
            serialized.data, context)


class GRPCResource(Resource):
    parser_classes = (GRPCMessageParser,)
    renderer_classes = (GRPCMessageRenderer,)


@api.route(uri='/grpc_book_service/query_books_post', methods=['POST'])
class QueryBooksPost(GRPCResource):
    name = 'grpc_book_service.query_books_post'
    req_schema = schemas.QueryBooksRequestSchema()
    resp_schema = schemas.BookSchema()

    def create(self, request):
        return grpc_book_service.query_books_post(request.data)


@api.route(uri='/grpc_book_service/get_book_post', methods=['POST'])
class GetBookPost(GRPCResource):
    name = 'grpc_book_service.get_book_post'
    req_schema = schemas.GetBookRequestSchema()
    resp_schema = schemas.BookSchema()

    def create(self, request):
        return grpc_book_service.get_book_post(request.data)
