import os
import subprocess

from django.conf import settings
from django.core.management import BaseCommand


def run(cmd, env=None, **kwargs):
    print(cmd)
    env = env or {}
    return subprocess.run(cmd, shell=True, env=dict(os.environ, **env), **kwargs)


dump_dir = os.path.join(settings.ROOT_DIR, ".dump")
FILENAME = "dump.sql"
os.makedirs(dump_dir, exist_ok=True)
DB_DUMP_FILEPATH = os.path.join(dump_dir, FILENAME)

METHODS = METHOD_DUMP, METHOD_LOAD = "dump", "load"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("method", type=str, choices=METHODS)
        parser.add_argument("--database", default="default")

    def _db_cmd(self, method, database):
        db_info = settings.DATABASES[database]
        host = db_info["HOST"]
        port = db_info["PORT"]
        db = db_info["NAME"]
        user = db_info["USER"]
        password = db_info["PASSWORD"]

        if method == METHOD_DUMP:
            run(
                f"pg_dump -h {host} -Fc {db} -U {user} > {DB_DUMP_FILEPATH}",
                env={"PGPASSWORD": password},
                check=True,
            )
        elif method == METHOD_LOAD:
            run(
                f"dropdb -h {host} -U {user} {db}",
                env={"PGPASSWORD": password},
                check=True,
            )
            run(
                f"createdb -h {host} -U {user} -T template0 -l C -e {db}",
                env={"PGPASSWORD": password},
                check=True,
            )
            run(
                f"pg_restore -h {host} -d {db} -U {user} {DB_DUMP_FILEPATH}",
                env={"PGPASSWORD": password},
                check=True,
            )

    def handle(self, *args, **options):
        method = options["method"]
        database = options["database"]
        try:
            self._db_cmd(method, database)
        finally:
            try:
                if method == METHOD_LOAD:
                    os.remove(DB_DUMP_FILEPATH)
            except OSError:
                pass
