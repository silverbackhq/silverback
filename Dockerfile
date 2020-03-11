FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

RUN rm -rf ./assets

EXPOSE 8000

VOLUME /app/storage

HEALTHCHECK --interval=5s --timeout=2s --retries=5 --start-period=2s \
  CMD python manage.py health check

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app.wsgi"]