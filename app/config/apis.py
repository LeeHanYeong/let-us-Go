import os
from subprocess import run, PIPE

from drf_yasg.openapi import Response as APIResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

FRONT_DIR = os.path.join(os.sep, 'srv', 'front')


class FrontDeployAPIView(APIView):
    """
    FrontDeploy

    ---
    ### Api-Key Authorization이 반드시 필요

    **`Authorization: Api-Key <key>`**

    위와 같이 `Authorization`헤더의 값으로 `Api-Key <key>`을 적용한다.
    (Api-Key문자열 다음 공백 한칸, 이후 바로 key값을 입력)

    서버에서 차례대로 아래 명령어들을 실행한다
    - `git pull`
    - `git rev-parse HEAD`
    - `npm run build`
    - `pm2 restart Yuni-Q_letusgo`
    - `pm2 list`

    Response에는 명령어 실행의 return code, stdout, stderr값이 담겨있으며,
    `git rev-parse HEAD`로 돌아온 마지막 커밋의 Hash값을 사용해 배포된 코드 버전을 알 수 있다.
    """
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: APIResponse(
                description='성공',
                examples={
                    'application/json': {
                        '명령어의 종류': {
                            'returncode': '실행한 명령어의 return code',
                            'stdout': '실행한 명령의 stdout메시지',
                            'stderr': '실행한 명령의 stderr메시지',
                        }
                    }
                }
            )
        }
    )
    def post(self, request):
        class Subprocess:
            OPTIONS = {
                'stdout': PIPE,
                'stderr': PIPE,
                'shell': True,
            }

            def __init__(self, name, command, options=None):
                self.name = name
                self.command = command
                self.options = self.OPTIONS.copy()
                if options:
                    self.options.update(**options)
                self._result = None

            def run(self):
                self._result = run(self.command, **self.options)
                return self._result

            @property
            def result(self):
                if not self._result:
                    self.run()
                return self._result

        os.chdir(FRONT_DIR)
        subprocess_list = (
            Subprocess('git_pull', 'git pull'),
            Subprocess('git_last_commit', 'git rev-parse HEAD'),
            Subprocess('npm_build', 'npm run build'),
            Subprocess('pm2_restart', 'pm2 restart Yuni-Q_letusgo'),
            Subprocess('pm2_list', 'pm2 list'),
        )
        results = {command.name: command.result for command in subprocess_list}
        data = {
            key: {
                'returncode': result.returncode,
                'stdout': result.stdout.decode('utf-8'),
                'stderr': result.stderr.decode('utf-8'),
            } for key, result in results.items(),
        }
        return Response(data)
