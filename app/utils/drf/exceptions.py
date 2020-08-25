from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError


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
