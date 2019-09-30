FROM python:3.7 as silverback-stage-1
MAINTAINER sourabh.deshmukh.988@gmail.com
ENV PYTHONUNBUFFERED 1
ARG VERSION=master
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN echo "yes" | python manage.py collectstatic


FROM silverback-stage-1 as silverback-stage-2
WORKDIR /app
EXPOSE 8000
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app.wsgi"]
