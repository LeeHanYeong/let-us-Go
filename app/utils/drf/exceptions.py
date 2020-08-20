from rest_framework.views import exception_handler


def rest_exception_handler(exc, context):
    # 클라이언트에서 status및 code활용
    response = exception_handler(exc, context)
    return response
