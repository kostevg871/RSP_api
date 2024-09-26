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

#RUN wget https://github.com/Kitware/CMake/releases/download/v3.24.2/cmake-3.24.2-linux-x86_64.tar.gz \
#&& rm -rf /usr/local/man \    
#&& tar -zxvf cmake-3.24.2-linux-x86_64.tar.gz \
#    && rm cmake-3.24.2-linux-x86_64.tar.gz \
#    && cp -r cmake-3.24.2-linux-x86_64/* /usr/local/ \ 
#    && rm -rf cmake-3.24.2-linux-x86_64 
	


#RUN apt-get update && apt-get install -y openssh-client

# Создание директории для SSH
#RUN mkdir -p ~/.ssh

# Добавление GitHub в known_hosts
#RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

# Добавление ключа SSH
#COPY /path/to/your/private/key /root/.ssh/id_rsa
#RUN chmod 600 /root/.ssh/id_rsa

# Очередная команда для доступа к GitHub
#RUN ssh -T git@github.com
RUN mkdir /RSP


WORKDIR /RSP

RUN pip install poetry
RUN pip install cmake
#RUN pip install Cmake

# Копируем SSH-ключи и known_hosts
## Убедитесь, что вы скопировали ваш id_rsa и known_hosts в подходящую директорию
COPY --chown=root:root /ssh_keys/rsp_deploy /root/.ssh/id_rsa
COPY --chown=root:root /ssh_keys/known_hosts /root/.ssh/known_hosts
COPY --chown=root:root /ssh_keys/rsp_deploy.pub /root/.ssh/id_rsa.pub


## Устанавливаем права доступа
RUN chmod 600 /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa.pub
RUN chmod 644 /root/.ssh/known_hosts \
&& ssh-keyscan github.com >> /root/.ssh/known_hosts

#RUN ssh -T git@github-librsp || true
# Клонируем приватный репозиторий (замените "your_username" и "your_repo" на ваши данные)
RUN git clone git@github.com:fiztexlabs/librsp.git

# Переходим в директорию с кодом
WORKDIR /RSP/librsp
RUN git submodule update --init --recursive

# Выполняем команду сборки CMake
#RUN cmake . && make
RUN cd .. 
RUN pip install .

WORKDIR /RSP

#RUN bash "ping google.com"
#RUN ssh -T git@github.com

ADD pyproject.toml poetry.lock ./

#RUN --mount=type=ssh bash -c 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts'
#RUN --mount=type=ssh mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
#RUN --mount=type=ssh  ssh -T git@github.com
#RUN --mount=type=ssh git clone git@github.com:fiztexlabs/librsp.git


RUN --mount=type=ssh \
       poetry config virtualenvs.create false && \
       poetry install --no-interaction --no-ansi --no-root -v


COPY . .

RUN chmod a+x /RSP/docker/*.sh

#CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]