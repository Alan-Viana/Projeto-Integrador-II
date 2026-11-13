"""Entidades da Área Restrita."""
from django.conf import settings
from django.db import models


class Usuario(models.Model):
    """Funcionário da ONG com acesso à Área Restrita.

    A autenticação (login, senha criptografada, sessão) usa o usuário padrão
    do Django; esta entidade guarda os dados de perfil do funcionário.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    nome = models.CharField(max_length=150)
    cargo = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome
