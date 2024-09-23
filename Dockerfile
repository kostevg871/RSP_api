FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /RSP

RUN apt-get update && \
	apt install -y python3-dev && \
	apt-get -y install cmake protobuf-compiler

RUN pip install --upgrade pip 
#RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts


ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh && chmod -R 700 /root/.ssh
RUN /bin/bash -c cat "${SSH_PRIVATE_KEY}" >> /root/.ssh/id_rsa 
RUN chmod 600 /root/.ssh/id_rsa && echo "StrictHostKeyChecking no" > /root/.ssh/config
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

#RUN git clone git@github.com:fiztexlabs/librsp.git

RUN pip install rsp
RUN pip install poetry

ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]

