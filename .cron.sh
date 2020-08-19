#!/usr/bin/env bash
cp -f .scripts/ssl_renew.sh /etc/cron.monthly
chmod +x /etc/cron.monthly/ssl_renew.sh
