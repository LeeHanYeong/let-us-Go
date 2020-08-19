docker run --rm -it \
      --env AWS_ACCESS_KEY_ID='$AWS_ROUTE53_ACCESS_KEY_ID' \
      --env AWS_SECRET_ACCESS_KEY='$AWS_ROUTE53_SECRET_ACCESS_KEY' \
      -v '/etc/letsencrypt:/etc/letsencrypt' \
      -v '/var/lib/letsencrypt:/var/lib/letsencrypt' \
      certbot/dns-route53 certificates
