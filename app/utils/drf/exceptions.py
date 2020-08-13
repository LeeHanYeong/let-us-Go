from django.http import Http404
from django.utils.encoding import force_str
from rest_framework import exceptions, status
from rest_framework.exceptions import APIException as BaseAPIException, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import set_rollback

from utils.drf.errors import Error
from . import errors


def _get_message(detail):
    if isinstance(detail, list):
        return '\n'.join([_get_message(item) for item in detail])
    elif isinstance(detail, dict):
        return '\n'.join([_get_message(value) for key, value in detail.items()])
    elif isinstance(detail, Error):
        return detail.message
    text = force_str(detail)
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
            'code': getattr(exc.detail, 'code', errors.UNDEFINED.code),
            'detail': getattr(exc.detail, 'message', exc.detail),
            'message': _get_message(exc.detail),
        }
        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    return None


class APIException(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        if isinstance(detail, Error):
            self.detail = detail


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
