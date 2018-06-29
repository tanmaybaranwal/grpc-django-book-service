import time
from contextlib import contextmanager

import grpc
from concurrent import futures
from django.core.management import BaseCommand

from grpc_book_service.grpc_protos import app_pb2_grpc
from grpc_book_service.grpc_protos.service_handler import BookService


class Command(BaseCommand):
    help = "Starts the GRPC server"

    def add_arguments(self, parser):
        parser.add_argument(
            "project", nargs=1,
            help="Django project settings path"
        )
        parser.add_argument(
            "port", nargs="?",
            help="Optional port number"
        )
        parser.add_argument(
            "--workers", dest="max_workers",
            help="Number of maximum worker threads"
        )

    @contextmanager
    def serve_forever(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        app_pb2_grpc.add_GRPCBookServiceServicer_to_server(
            BookService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        yield
        server.stop(0)

    def handle(self, *args, **options):
        with self.serve_forever():
            self.stdout.write(
                self.style.SUCCESS('Successfully started grpc server '))
            try:
                while True:
                    time.sleep(60 * 60 * 24)
            except KeyboardInterrupt:
                pass
