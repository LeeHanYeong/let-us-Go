import os
from subprocess import run, PIPE

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

FRONT_DIR = os.path.join(os.sep, 'srv', 'front')


class FrontDeployAPIView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request):
        os.chdir(FRONT_DIR)
        result_pull = run('git pull', stdout=PIPE, stderr=PIPE, shell=True)
        result_restart = run('pm2 restart Yuni-Q_letusgo', stdout=PIPE, stderr=PIPE, shell=True)
        data = {
            'pull': {
                'returncode': result_pull.returncode,
                'stdout': result_pull.stdout,
                'stderr': result_pull.stderr,
            },
            'restart': {
                'returncode': result_restart.returncode,
                'stdout': result_restart.stdout,
                'stderr': result_restart.stderr,
            },
        }
        return Response(data)
