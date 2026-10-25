"""
Camada de Service da aplicação principal (core).

Mantém a mesma convenção adotada em servicos/services.py: a view
(controller) nunca deve conter regras de negócio, apenas orquestrar a
chamada aos serviços apropriados.
"""
from __future__ import annotations

import logging

from .forms import ContatoForm

logger = logging.getLogger(__name__)


class ContatoService:
    """Regras de negócio relacionadas ao envio de mensagens de contato."""

    def processar_mensagem(self, form: ContatoForm) -> None:
        """Processa uma mensagem de contato válida.

        Por enquanto, a mensagem é apenas registrada em log. Em uma
        próxima etapa do projeto, este método passará a persistir a
        mensagem no banco de dados e/ou integrá-la a um serviço de
        e-mail transacional.
        """
        dados = form.cleaned_data
        logger.info(
            "Nova mensagem de contato recebida de %s <%s> - assunto: %s",
            dados["nome_completo"],
            dados["email"],
            dados["assunto"],
        )
