FROM python:3.12.3
#FROM alpine:latest

COPY . .

ENV APP_ENV="${KEY_RSP}"

#RUN apk --no-cache add git \ 
#	&& git clone https://fiztexlabs:${APP_ENV}@github.com https://github.com/fiztexlabs/librsp.git

RUN pip install git+https://${APP_ENV}@github.com/fiztexlabs/librsp.git
RUN pip install -r requirements.txt

CMD ["uvicorn", "main.py", "--host", "--port", "80"]