FROM nginx
ARG build_const_path="./constants/local_constants.js"
ARG port=8080
ARG nginx_config_path="local_default.conf"
COPY ./static /usr/share/nginx/html/
COPY ${build_const_path} /usr/share/nginx/html/constants/constants.js
EXPOSE ${port}
ADD ${nginx_config_path} /etc/nginx/conf.d/default.conf
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
