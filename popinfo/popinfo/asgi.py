"""Configuração ASGI para o projeto PopInfo."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "popinfo.settings")

application = get_asgi_application()
