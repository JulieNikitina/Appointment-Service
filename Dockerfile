FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY wait-for /code/
RUN chmod +x /code/wait-for
RUN apk add --update --no-cache postgresql-libs
RUN apk add --update --no-cache --virtual .tmp musl-dev postgresql-dev gcc libc-dev linux-headers
RUN pip install -r requirements.txt
COPY . /code/