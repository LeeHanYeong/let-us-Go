from django.http import Http404
from django.utils.encoding import force_text
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException as BaseAPIException, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import set_rollback

from . import errors


def _get_message(detail):
    if isinstance(detail, list):
        return '\n'.join([_get_message(item) for item in detail])
    elif isinstance(detail, dict):
        return '\n'.join([_get_message(value) for key, value in detail.items()])
    text = force_text(detail)
    return text


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, (BaseAPIException, APIException)):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = getattr(exc, 'auth_header')
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % getattr(exc, 'wait')

        data = {
            'code': getattr(exc, 'errors', errors.UNDEFINED).code,
            'detail': exc.detail,
            'message': _get_message(exc.detail),
        }
        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    return None


class APIException(BaseAPIException):
    def __init__(self, error=None, detail=None, code=None):
        self.error = error or errors.UNDEFINED
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ValidationError(APIException):
    def __init__(self, error=None, detail=None, code=status.HTTP_400_BAD_REQUEST):
        super().__init__(error=error, detail=detail, code=code)
