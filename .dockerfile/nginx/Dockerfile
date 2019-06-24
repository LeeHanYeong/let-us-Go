FROM nginx:stable-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.app.conf /etc/nginx/conf.d
COPY nginx.settings.conf /etc/nginx/conf.d
