FROM python:3-alpine

RUN apk update
RUN apk add --no-cache tzdata
RUN apk add gcc musl-dev mariadb-connector-c-dev
RUN apk add python3-dev build-base linux-headers pcre-dev

RUN python -m pip install --upgrade pip
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN pip install uwsgi

COPY ./hksova /usr/src/app/hksova
COPY ./configs/default.py /usr/src/app/configs/default.py
COPY ./configs/docker.py /usr/src/app/configs/docker.py
COPY ./configs/uwsgi/docker_wsgi.ini /usr/src/app/configs/uwsgi/docker_uwsgi.ini

ENV HKSOVA_CONFIG_DIR=/usr/src/app/configs
ENV HKSOVA_CONFIG=/usr/src/app/configs/docker.py
ENV TZ=Europe/Prague

EXPOSE 5000

CMD ["uwsgi", "--ini", "/usr/src/app/configs/uwsgi/docker_uwsgi.ini"]
