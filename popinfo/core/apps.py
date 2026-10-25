from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuração da aplicação principal (Início, Sobre, Contato)."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Núcleo do site"
