import uuid

import grpc
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, \
    ValidationError as DjangoValidationError


class GrpcException(Exception):
    """
    Base class for GRPC exceptions
    """
    status_code = grpc.StatusCode.INTERNAL
    default_message = "A server error occurred."

    def __init__(self, message):
        if message is None:
            self.message = self.default_message
        else:
            self.message = message

    def __str__(self):
        return self.message


class NotAuthenticated(GrpcException):
    status_code = grpc.StatusCode.UNAUTHENTICATED
    default_message = "Authentication credentials were not provided."


class AuthenticationFailed(GrpcException):
    status_code = grpc.StatusCode.UNAUTHENTICATED
    default_message = "Incorrect authentication credentials."


class PermissionDenied(GrpcException):
    status_code = grpc.StatusCode.PERMISSION_DENIED
    default_message = "You do not have permission to perform this action."


class InvalidArgument(GrpcException):
    status_code = grpc.StatusCode.INVALID_ARGUMENT
    default_message = "Invalid input."


class ValidationError(GrpcException):
    status_code = grpc.StatusCode.FAILED_PRECONDITION
    default_message = "Invalid input."


class ExceptionHandler(object):
    _handlers = {
        ObjectDoesNotExist: (grpc.StatusCode.NOT_FOUND, str),
        MultipleObjectsReturned: (
            grpc.StatusCode.ALREADY_EXISTS, str),
        DjangoValidationError: (
            grpc.StatusCode.FAILED_PRECONDITION, str),
    }

    def __init__(self, context):
        self.context = context

    def __call__(self, exc, stack):
        if issubclass(exc.__class__, GrpcException):
            status_code, message = exc.status_code, str(exc)
        elif self._handlers.get(exc.__class__):
            status_code, message = self._handlers[exc.__class__][0], \
                                   self._handlers[exc.__class__][1](exc)
        else:
            status_code = grpc.StatusCode.UNKNOWN
            message = "{}; ErrorId: {}".format(exc, uuid.uuid4())
        self.context.set_code(status_code)
        self.context.set_details(message)
        return self.context
