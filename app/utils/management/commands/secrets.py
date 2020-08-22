import json
import os
import shutil
from pathlib import Path
from pprint import pprint

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--force", action="store_true", help="Force update by local secrets"
        )

    def handle(self, *args, **options):
        project = settings.PROJECT

        home = str(Path.home())
        dropbox_dir = os.path.join(home, "Dropbox", "settings", "django", project)
        if options["force"]:
            shutil.rmtree(dropbox_dir)
        os.makedirs(dropbox_dir, exist_ok=True)

        dropbox_filename_set = {
            filename for filename in os.listdir(dropbox_dir) if ".json" in filename
        }
        secrets_filename_set = {
            filename
            for filename in os.listdir(settings.SECRETS_DIR)
            if ".json" in filename
        }
        filename_list = list(dropbox_filename_set | secrets_filename_set)

        secrets = {}
        for filename in filename_list:
            dropbox_file_path = os.path.join(dropbox_dir, filename)
            secrets_file_path = os.path.join(settings.SECRETS_DIR, filename)

            secrets_dict = {}
            if os.path.isfile(secrets_file_path):
                secrets_dict = json.load(open(secrets_file_path))

            dropbox_dict = {}
            if os.path.isfile(dropbox_file_path):
                dropbox_dict = json.load(open(dropbox_file_path))
            for secret_key, secret_value in secrets_dict.items():
                dropbox_value = dropbox_dict.get(secret_key)
                # Dropbox에 local의 key에 해당하는 값이 없거나 빈 값일 경우에만 덮어씌움
                if not dropbox_value:
                    dropbox_dict[secret_key] = secret_value

            # 작성한 secrets를 local과 Dropbox에 동시저장
            json.dump(dropbox_dict, open(dropbox_file_path, "wt"), indent=2)
            json.dump(dropbox_dict, open(secrets_file_path, "wt"), indent=2)
            secrets[filename] = dropbox_dict
        pprint(secrets)
