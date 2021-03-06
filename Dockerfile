FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y curl build-essential software-properties-common && \
    curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python3 python3-venv python3-dev python3-pip \
                       libpq-dev supervisor \
                       git nginx nodejs postgresql-client && \
    ln -s /usr/bin/python3 /usr/bin/python && \ 
    ln -s /usr/bin/pip3 /usr/bin/pip && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    useradd --create-home --shell /bin/bash skyportal

RUN python3 -m venv /skyportal_env && \
    \
    bash -c "source /skyportal_env/bin/activate && \
    pip install --upgrade pip"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ADD . /skyportal
WORKDIR /skyportal

RUN bash -c "\
    source /skyportal_env/bin/activate && \
    \
    make -C baselayer paths && \
    (make -f baselayer/Makefile baselayer dependencies || make -C baselayer dependencies) && \
    (make -f baselayer/Makefile baselayer fill_conf_values || make -C baselayer fill_conf_values)"

RUN bash -c "\
    \
    ./node_modules/.bin/webpack --mode=production --devtool none && \
    rm -rf node_modules && \
    \
    chown -R skyportal.skyportal /skyportal_env && \
    chown -R skyportal.skyportal /skyportal && \
    chmod -R 777 /skyportal  /skyportal_env && \
    mkdir -p log run tmp ./log/sv_child && \
    chown -R skyportal.skyportal log run tmp ./log/sv_child && \
    chmod -R 777 log run tmp ./log/sv_child && \
    chown skyportal.skyportal / && \
    mkdir -p  /.npm && \
    chown -R 5213:0 /.npm && \
    \
    mkdir -p /skyportal/static/thumbnails && \
    chown -R skyportal.skyportal /skyportal/static/thumbnails && \
    \
    cp docker.yaml config.yaml && \
    \
    chmod +x docker-entrypoint.sh"

USER skyportal

EXPOSE 5000

CMD bash -c "source /skyportal_env/bin/activate && \
             (make log &) && \
             make run_production"

ENTRYPOINT ["./docker-entrypoint.sh"]
