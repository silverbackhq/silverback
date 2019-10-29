FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

RUN rm -rf ./assets

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app.wsgi"]
