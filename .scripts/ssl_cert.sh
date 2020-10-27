docker run --rm -it \
      --env AWS_ACCESS_KEY_ID='$AWS_ROUTE53_ACCESS_KEY_ID' \
      --env AWS_SECRET_ACCESS_KEY='$AWS_ROUTE53_SECRET_ACCESS_KEY' \
      -v '/etc/letsencrypt:/etc/letsencrypt' \
      -v '/var/lib/letsencrypt:/var/lib/letsencrypt' \
      certbot/dns-route53 certonly --dns-route53 \
      -d '*.letusgo.app' \
      -d api.letusgo.app \
      -d api.dev.letusgo.app \
      -d api.feature.letusgo.app \
      -d letusgo.app \
      --agree-tos
