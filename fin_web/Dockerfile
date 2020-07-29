FROM python:3.6.6-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update \
    && apk add libxml2 postgresql-dev linux-headers libevent-dev g++ gcc jpeg-dev zlib-dev libxslt-dev gcc python3-dev musl-dev

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN chmod +x /code/scheduler/run.sh /code/entrypoint.sh

