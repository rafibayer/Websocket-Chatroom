FROM python:3.8
LABEL maintainer="Rafi Bayer rafibayer7@gmail.com"

# Configs to copy for server, defaults to local
ARG configpath="/config/local_config" 
RUN pip install pipenv
COPY Pipfile* /tmp/

# Install dependencies
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY /server /server
COPY $configpath /config
EXPOSE 80
WORKDIR /server

# Start server
# -(U)nbuffered output flag to see print logs in docker logs
CMD [ "python", "-u", "app.py" ]

