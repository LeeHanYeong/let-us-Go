#!/usr/bin/env python
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("branch")
args = parser.parse_args()


def run(cmd, **kwargs):
    subprocess.run(cmd, shell=True, **kwargs)


if __name__ == "__main__":
    branch = args.branch
    run(f"git fetch --all")
    run(f"git checkout {branch}")
    run(f"git pull origin {branch}")
    run(f"sudo cp -f .scripts/ssl_renew.sh /etc/cron.monthly")
    run(f"docker-compose build django_{branch}")
    run(f"docker-compose stop django_{branch}")
    run(
        f"docker-compose -p letusgo up --force-recreate --remove-orphans -d django_{branch}"
    )
    run(f"docker system prune -a --volumes -f")
    if branch == "feature":
        run(f"docker-compose -p letusgo up --force-recreate -d nginx")
    print("Update complete")
