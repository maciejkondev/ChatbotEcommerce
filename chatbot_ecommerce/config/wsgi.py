"""
WSGI config for chatbot_ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Ustawienie zmiennej środowiskowej DJANGO_SETTINGS_MODULE na config.settings

application = get_wsgi_application()
