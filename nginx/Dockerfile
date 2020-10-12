FROM nginx:latest
EXPOSE 80

RUN rm /etc/nginx/conf.d/*.conf
COPY b2share-dev.conf /etc/nginx/conf.d/

CMD ["nginx","-g","daemon off;"]
