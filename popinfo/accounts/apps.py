from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuração da aplicação de autenticação (Área Restrita)."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Contas"
