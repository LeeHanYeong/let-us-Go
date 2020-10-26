from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError, _get_full_details
from rest_framework.response import Response
from rest_framework.views import set_rollback


def rest_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        data = _get_full_details(exc.detail)
        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    return None


class InvalidCredentials(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "인증정보가 올바르지 않습니다"
    default_code = "invalid_credentials"


class OAuthUserNotRegistered(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "해당 OAuth서비스에 등록된 사용자가 없습니다"
    default_code = "oauth_user_not_registered"


class EmailSendFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "이메일 전송에 실패했습니다"
    default_code = "email_send_failed"


class EmailVerificationDoesNotExist(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이메일 인증정보가 존재하지 않습니다"
    default_code = "email_verification_does_not_exist"


class EmailVerificationCodeInvalid(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이메일 인증코드가 유효하지 않습니다"
    default_code = "email_verification_code_invalid"
