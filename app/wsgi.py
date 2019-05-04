"""
WSGI Config for Silverback

It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/

To Run Using gunicorn
pip install gunicorn
gunicorn app.wsgi:application
"""

# Standard Library
import os

# Third Party Library
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.basic")

application = get_wsgi_application()
