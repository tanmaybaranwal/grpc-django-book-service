# -*- coding: utf-8 -*-

import enum
import grpc

import grpc_book_service.grpc_protos.app_pb2
import grpc_book_service.grpc_protos.app_pb2_grpc


class BookTypeEnum(enum.Enum):
    PAPER_BACK = 0
    HARD_BIND = 1
    ONLINE = 2


Publication = grpc_book_service.grpc_protos.app_pb2.Publication
Book = grpc_book_service.grpc_protos.app_pb2.Book
QueryBooksRequest = grpc_book_service.grpc_protos.app_pb2.QueryBooksRequest
GetBookRequest = grpc_book_service.grpc_protos.app_pb2.GetBookRequest


class GRPCBookService(object):

    def __init__(self, target, timeout=10):
        self.target = target
        self.timeout = timeout

    @property
    def stub(self):
        channel = grpc.insecure_channel(self.target)
        return grpc_book_service.grpc_protos.app_pb2_grpc.GRPCBookServiceStub(
            channel)

    def call_rpc(self, rpc_name, req):
        rpc = getattr(self.stub, rpc_name)
        resp = rpc(req, self.timeout)
        return resp

    def query_books_post(self, query_books_request):
        resp = self.call_rpc('QueryBooksPost', query_books_request)
        return resp

    def get_book_post(self, get_book_request):
        resp = self.call_rpc('GetBookPost', get_book_request)
        return resp
