#!/usr/bin/env bash
git pull
sudo cp -f .scripts/ssl_renew.sh /etc/cron.monthly
sudo chmod +x /etc/cron.monthly/ssl_renew.sh
docker-compose build
docker-compose restart
docker system prune -a --volumes -f
