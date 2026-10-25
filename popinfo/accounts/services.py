"""Camada de Service da aplicação de autenticação."""
from __future__ import annotations

from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class AutenticacaoService:
    """Regras de negócio relacionadas à autenticação de usuários."""

    def autenticar(self, email: str, senha: str) -> User | None:
        """Autentica um usuário da Área Restrita pelo e-mail e senha.

        Usuários administrativos devem ser criados com o e-mail também
        preenchido no campo "username" (comportamento padrão de
        `createsuperuser` ao informar o e-mail quando solicitado).
        """
        return authenticate(username=email, password=senha)
