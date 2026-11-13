"""Camada de Service da aplicação de autenticação."""
from __future__ import annotations

from django.contrib.auth import authenticate, get_user_model


class AutenticacaoService:
    """Regras de negócio relacionadas à autenticação de usuários."""

    def autenticar(self, email: str, senha: str):
        """Autentica pelo nome de usuário ou, se não houver, pelo e-mail."""
        usuario = authenticate(username=email, password=senha)
        if usuario is None and "@" in email:
            conta = get_user_model().objects.filter(email__iexact=email).first()
            if conta:
                usuario = authenticate(username=conta.username, password=senha)
        return usuario
