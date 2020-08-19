from rest_framework.views import exception_handler


def rest_exception_handler(exc, context):
    # 클라이언트에서 status및 code활용
    response = exception_handler(exc, context)
    if response:
        response.data['status'] = response.status_code
        # Exception에 'code'가 존재할 경우 해당 내용
        # 없으면 Response의 ErrorDetail이 가지고 있는 'code'값
        response.data['code'] = getattr(exc, 'code', getattr(exc, 'default_code', None)) or response.data['detail'].code
    return response
