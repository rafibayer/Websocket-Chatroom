FROM nginx
LABEL maintainer="Rafi Bayer rafibayer7@gmail.com"

# constants file for build, defaults to local
ARG build_const_path="./constants/local_constants.js"
# Port for build, defaults to 8080
ARG port=8080
# nginx conf for build, defaults to local
ARG nginx_config_path="local_default.conf"

# copy static content
COPY ./static /usr/share/nginx/html/
# copy constants
COPY ${build_const_path} /usr/share/nginx/html/constants/constants.js
EXPOSE ${port}
# copy nginx config
ADD ${nginx_config_path} /etc/nginx/conf.d/default.conf
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
