FROM python:3-alpine

RUN apk update
RUN apk add \
    tzdata \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    python3-dev \
    build-base \
    linux-headers \
    pcre-dev \
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && rm -f /var/cache/apk/*

# TODO:
# vylepsit ten buildstack, aby nebyl v image:
#RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
#RUN apk add --no-cache jpeg-dev zlib-dev
#RUN pip install -r /requirements.txt
#RUN apk del .tmp

RUN python -m pip install --upgrade pip
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN pip install uwsgi

# used volume mount to prevent restarts after each update
# probably copy is better...
# COPY ./hksova /usr/src/app/hksova
# ADD ./hksova /usr/src/app/hksova


COPY ./configs/default.py /usr/src/app/configs/default.py
COPY ./configs/docker.py /usr/src/app/configs/docker.py
COPY ./configs/uwsgi/docker_wsgi.ini /usr/src/app/configs/uwsgi/docker_uwsgi.ini

RUN addgroup -S hksova && adduser -u 2000 -S hksova -G hksova

ENV HKSOVA_CONFIG_DIR=/usr/src/app/configs
ENV HKSOVA_CONFIG=/usr/src/app/configs/docker.py
ENV TZ=Europe/Prague

EXPOSE 5000

# stale to pri startu containeru pinda, ze chces --uid flag...
CMD ["uwsgi", "--ini", "/usr/src/app/configs/uwsgi/docker_uwsgi.ini", "--uid", "2000"]
