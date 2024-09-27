# syntax=docker/dockerfile:1.2
FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN apt-get update && apt-get install -y \
build-essential \
    cmake \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN mkdir /RSP


WORKDIR /RSP

RUN pip install poetry
RUN pip install cmake

#COPY --chown=root:root /ssh_keys/rsp_deploy /root/.ssh/id_rsa
#COPY --chown=root:root /ssh_keys/known_hosts /root/.ssh/known_hosts
#COPY --chown=root:root /ssh_keys/rsp_deploy.pub /root/.ssh/id_rsa.pub



#RUN chmod 600 /root/.ssh/id_rsa
#RUN chmod 600 /root/.ssh/id_rsa.pub
#RUN chmod 644 /root/.ssh/known_hosts \
#&& ssh-keyscan github.com >> /root/.ssh/known_hosts


RUN --mount=type=secret,id=ssh_key \
    mkdir -p /root/.ssh && \
    cp /run/secrets/ssh_key /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
	ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    git clone git@github.com:fiztexlabs/librsp.git

#RUN git clone git@github.com:fiztexlabs/librsp.git


WORKDIR /RSP/librsp
RUN git submodule update --init --recursive


RUN cd .. 
RUN pip install .

WORKDIR /RSP



ADD pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false && \
       poetry install --no-interaction --no-ansi --no-root -v


COPY . .

RUN chmod a+x /RSP/docker/*.sh

