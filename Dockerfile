FROM registry.esav.fi/base/python3
MAINTAINER Esa Varemo <esa@kuivanto.fi>

RUN pip3 install jsonpickle python-dateutil pytz requests

ENV APP_GIT=https://github.com/varesa/mustikkaBot.git

ENV APP=mustikkabot

RUN useradd $APP
RUN mkdir /$APP && chown $APP:$APP /$APP
USER $APP

ENV GIT_COMMITTER_NAME=$APP  GIT_COMMITTER_EMAIL=$APP@localhost
RUN git clone $APP_GIT /$APP

WORKDIR /$APP/src
CMD ["/usr/bin/python3", "main.py"]

VOLUME /$APP/config
VOLUME /$APP/data
