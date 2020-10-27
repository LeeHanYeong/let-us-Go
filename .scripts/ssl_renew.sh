echo "Renew | $(date +'%Y.%m.%d %H:%M:%S')" >> /home/ubuntu/ssl.txt
export $(cat .env | xargs) && docker run --rm -it \
      --env AWS_ACCESS_KEY_ID=$(echo "$AWS_ROUTE53_ACCESS_KEY_ID") \
      --env AWS_SECRET_ACCESS_KEY=$(echo "$AWS_ROUTE53_SECRET_ACCESS_KEY") \
      -v '/etc/letsencrypt:/etc/letsencrypt' \
      -v '/var/lib/letsencrypt:/var/lib/letsencrypt' \
      certbot/dns-route53 renew --dns-route53 \
      --agree-tos
