FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



RUN apt-get update && apt-get install -y \
    cmake \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

#RUN wget https://github.com/Kitware/CMake/releases/download/v3.24.2/cmake-3.24.2-linux-x86_64.tar.gz \
#&& rm -rf /usr/local/man \    
#&& tar -zxvf cmake-3.24.2-linux-x86_64.tar.gz \
#    && rm cmake-3.24.2-linux-x86_64.tar.gz \
#    && cp -r cmake-3.24.2-linux-x86_64/* /usr/local/ \ 
#    && rm -rf cmake-3.24.2-linux-x86_64 
	
#RUN pip install cmake
RUN mkdir /RSP


WORKDIR /RSP

RUN pip install poetry

#RUN pip install Cmake

# Копируем SSH-ключи и known_hosts
## Убедитесь, что вы скопировали ваш id_rsa и known_hosts в подходящую директорию
#COPY --chown=root:root /ssh_keys/rsp_deploy /root/.ssh/id_rsa
#COPY --chown=root:root /ssh_keys/known_hosts /root/.ssh/known_hosts
#COPY --chown=root:root /ssh_keys/rsp_deploy.pub /root/.ssh/id_rsa.pub


## Устанавливаем права доступа
#RUN chmod 600 /root/.ssh/id_rsa
#RUN chmod 600 /root/.ssh/id_rsa.pub
#RUN chmod 644 /root/.ssh/known_hosts \
#&& ssh-keyscan github.com >> /root/.ssh/known_hosts

#RUN ssh -T git@github-librsp || true
# Клонируем приватный репозиторий (замените "your_username" и "your_repo" на ваши данные)
#RUN git clone git@github.com:fiztexlabs/librsp.git

# Переходим в директорию с кодом
#WORKDIR /RSP/librsp
#RUN git submodule update --init --recursive

# Выполняем команду сборки CMake
#RUN cmake . && make


#RUN ssh -T git@github.com

ADD pyproject.toml poetry.lock ./

RUN --mount=type=ssh bash -c 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts'

RUN poetry config cache-dir /var/cache/pypoetry
RUN poetry install --no-dev


COPY . .

#RUN chmod a+x /docker/*.sho