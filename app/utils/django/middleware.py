from django.middleware.common import CommonMiddleware

__all__ = (
    'AppendSlashMiddleware',
)


class AppendSlashMiddleware(CommonMiddleware):
    """
    요청 URL의 마지막이 '/'가 없는 경우, 강제로 붙여준다
    """

    def process_request(self, request):
        if not request.path.endswith('/'):
            request.path += '/'
        if not request.path_info.endswith('/'):
            request.path_info += '/'
