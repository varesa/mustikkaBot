FROM python:3
MAINTAINER Esa Varemo <esa@kuivanto.fi>

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY . /app

RUN chown 974 /app/data /app/config -R
USER 974

WORKDIR /app/src
CMD ["/usr/bin/env", "python3", "main.py"]

VOLUME /app/config
VOLUME /app/data
