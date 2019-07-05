release: bash postdeploy.sh
web: python manage.py collectstatic --noinput; gunicorn app.wsgi --log-file -
