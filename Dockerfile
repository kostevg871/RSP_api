FROM ubuntu:20.04

ARG PYTHON_VER=3.12
ARG GCC_VER=13

RUN apt-get update && apt-get install -y software-properties-common curl nano

RUN add-apt-repository ppa:ubuntu-toolchain-r/test \
    && apt-get update \
    && apt-get install -y "gcc-$GCC_VER" "g++-$GCC_VER"

RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y "python$PYTHON_VER" "python$PYTHON_VER-venv" "python$PYTHON_VER-dev" "python$PYTHON_VER-distutils"

RUN apt-get update && apt-get install -y pip && pip install --upgrade pip

RUN apt-get clean

WORKDIR /rsp

RUN pip install poetry


ADD pyproject.toml poetry.lock ./


RUN poetry env use $(which python3.12)

RUN poetry config virtualenvs.create false && \
       poetry install --no-interaction --no-ansi --no-root -v


COPY . .

RUN make download

RUN chmod a+x /rsp/docker/*.sh



#FROM ubuntu:22.04

## Установите необходимые зависимости
#RUN apt-get update && apt-get install -y wget \
#    build-essential \
#    libssl-dev \
#    libbz2-dev \
#    libreadline-dev \
#    libsqlite3-dev \
#    libffi-dev \
#    zlib1g-dev \
#    curl \
#    nano \
#    software-properties-common

## Установка gcc и g++
#ARG GCC_VER=13
#RUN add-apt-repository ppa:ubuntu-toolchain-r/test \
#    && apt-get update \
#    && apt-get install -y "gcc-$GCC_VER" "g++-$GCC_VER"

## Установка Python 3.12.3 из исходного кода
#ARG PYTHON_VER=3.12.3
#RUN wget https://www.python.org/ftp/python/$PYTHON_VER/Python-$PYTHON_VER.tgz && \
#    tar xzf Python-$PYTHON_VER.tgz &&  cd Python-$PYTHON_VER && \
#    ./configure --enable-optimizations && \
#    make -j $(nproc) &&  make altinstall && cd .. && rm -rf Python-$PYTHON_VER Python-$PYTHON_VER.tgz

## Установите pip
#RUN apt-get update && apt-get install -y python3-distutils && \
#    curl -sS https://bootstrap.pypa.io/get-pip.py | python3

## Обновление pip
#RUN pip3.12 install --upgrade pip

## Очистка
#RUN apt-get clean && rm -rf /var/lib/apt/lists/*

#WORKDIR /rsp
