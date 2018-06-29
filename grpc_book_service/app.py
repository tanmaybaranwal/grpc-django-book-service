from django.apps import AppConfig

class GrpcBookServiceAppConfig(AppConfig):
    name = "grpc_book_service"

    def ready(self):
        pass
