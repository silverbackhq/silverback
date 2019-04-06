FROM python:3.6

ENV PYTHONUNBUFFERED 1

ARG VERSION=master

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app.wsgi"]