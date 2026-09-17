FROM python:3-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague

RUN apt-get update && apt-get install --no-install-recommends -y \
        tzdata \
        locales \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff-dev \
        tk-dev \
        tcl-dev \
        libpcre2-dev \
        default-libmysqlclient-dev \
        pkg-config \
    && echo "cs_CZ.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen cs_CZ.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install --no-install-recommends -y build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN pip install --no-cache-dir uwsgi

RUN apt-get purge -y --auto-remove build-essential

RUN groupadd -r hksova && useradd -r -M -u 2000 -g hksova hksova

COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

ENV HKSOVA_CONFIG_DIR=/usr/src/app/configs
ENV HKSOVA_CONFIG=/usr/src/app/configs/docker.py

EXPOSE 5000

# stale to pri startu containeru pinda, ze chces --uid flag...
# script wait ocekava nastavenou env promennou WAIT_HOSTS a to o hodnote host:port, pripadne carkou oddelit vice
CMD ["/bin/sh", "-c", "/wait && uwsgi --ini /usr/src/app/configs/uwsgi/docker_uwsgi.ini --uid 2000"]
