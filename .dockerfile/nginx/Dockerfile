FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY ../../.config/nginx.app.conf /etc/nginx/conf.d
COPY ../../.config/nginx.settings.conf /etc/nginx/conf.d
