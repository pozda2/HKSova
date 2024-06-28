FROM python:3-alpine

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add tzdata
RUN apk add --no-cache jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev pcre-dev mariadb-connector-c-dev python3-dev

RUN python -m pip install --upgrade pip
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN pip install uwsgi

RUN apk del .tmp

RUN addgroup -S hksova && adduser -u 2000 -S hksova -G hksova

ENV HKSOVA_CONFIG_DIR=/usr/src/app/configs
ENV HKSOVA_CONFIG=/usr/src/app/configs/docker.py
ENV TZ=Europe/Prague

EXPOSE 5000

# stale to pri startu containeru pinda, ze chces --uid flag...
CMD ["uwsgi", "--ini", "/usr/src/app/configs/uwsgi/docker_uwsgi.ini", "--uid", "2000"]
