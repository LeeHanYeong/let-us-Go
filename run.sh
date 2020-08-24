#!/usr/bin/env bash
git fetch --all
git pull
sudo cp -f .scripts/ssl_renew.sh /etc/cron.monthly
sudo chmod +x /etc/cron.monthly/ssl_renew.sh
docker-compose build
docker-compose stop
docker-compose up --force-recreate --remove-orphans -d
docker system prune -a --volumes -f
