#!/usr/bin/env python
"""Utilitário de linha de comando do Django para o projeto PopInfo."""
import os
import sys


def main() -> None:
    """Executa tarefas administrativas do Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "popinfo.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Verifique se ele está "
            "instalado e disponível na variável de ambiente PYTHONPATH. "
            "Você ativou o ambiente virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
