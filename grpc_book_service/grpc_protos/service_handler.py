from grpc_book_service.grpc_protos import app_pb2_grpc, app_pb2
from grpc_book_service.grpc_utils.protobuf_to_dict import dict_to_protobuf, \
    protobuf_to_dict


class BookService(app_pb2_grpc.GRPCBookServiceServicer):
    def QueryBooksPost(self, request, context):
        print("Request is not a stream.")
        while 1:
            response = {
                "isbn": request.author_prefix,
                "name": "string",
                "title": "string",
                "author": "string",
                "book_type": "PAPER_BACK",
                "codes": [1.0, 2.5, 5.5],
                "metadata_ref": "string",
                "publication": {
                    "name": "string",
                    "email": "string"
                }
            }
            response = dict_to_protobuf(app_pb2.Book, response)
            yield response

    def GetBookPost(self, request, context):
        request_data = protobuf_to_dict(request)
        from grpc_book_service.views.get_book.api_wrapper import api_wrapper
        response = api_wrapper(request_data=request_data)
        response = dict_to_protobuf(app_pb2.Book, response)
        return response
