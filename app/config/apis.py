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
        result_git_pull = run('git pull', stdout=PIPE, stderr=PIPE, shell=True)
        result_git_last_commit = run('git rev-parse HEAD', stdout=PIPE, stderr=PIPE, shell=True)
        result_pm2_restart = run('pm2 restart Yuni-Q_letusgo', stdout=PIPE, stderr=PIPE, shell=True)
        result_pm2_list = run('pm2 list', stdout=PIPE, stderr=PIPE, shell=True)
        data = {
            'git_pull': {
                'returncode': result_git_pull.returncode,
                'stdout': result_git_pull.stdout.decode('utf-8'),
                'stderr': result_git_pull.stderr.decode('utf-8'),
            },
            'git_last_commit': {
                'returncode': result_git_last_commit.returncode,
                'stdout': result_git_last_commit.stdout.decode('utf-8'),
                'stderr': result_git_last_commit.stderr.decode('utf-8'),
            },
            'pm2_restart': {
                'returncode': result_pm2_restart.returncode,
                'stdout': result_pm2_restart.stdout.decode('utf-8'),
                'stderr': result_pm2_restart.stderr.decode('utf-8'),
            },
            'pm2_list': {
                'returncode': result_pm2_list.returncode,
                'stdout': result_pm2_list.stdout.decode('utf-8'),
                'stderr': result_pm2_list.stderr.decode('utf-8'),
            },
        }
        return Response(data)
