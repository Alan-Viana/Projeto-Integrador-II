"""Configuração WSGI para o projeto PopInfo."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "popinfo.settings")

application = get_wsgi_application()
