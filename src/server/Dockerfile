FROM python:3.8
LABEL maintainer="Rafi Bayer rafibayer7@gmail.com"
ARG configpath="/config" 
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY /server /server
COPY $configpath /config
EXPOSE 80
WORKDIR /server

# Unbuffered output flag to see print logs in docker logs
CMD [ "python", "-u", "server.py" ]

