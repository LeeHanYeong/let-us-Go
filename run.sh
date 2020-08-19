#!/usr/bin/env bash
sudo cp -f .scripts/ssl_renew.sh /etc/cron.monthly
sudo chmod +x /etc/cron.monthly/ssl_renew.sh
