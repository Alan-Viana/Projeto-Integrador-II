"""
Camada de Repository da aplicação Serviços.

Os repositórios isolam toda a interação com o ORM do Django (consultas ao
banco de dados). Nenhuma outra camada da aplicação deve importar os
modelos diretamente para fazer consultas — apenas os repositórios têm
essa responsabilidade. Isso facilita testes (é possível substituir o
repositório por um "fake" em memória) e futuras trocas de fonte de dados.
"""
from __future__ import annotations

from django.db.models import Q, QuerySet

from .models import Categoria, Servico


class CategoriaRepository:
    """Acesso a dados da entidade Categoria."""

    def listar_todas(self) -> QuerySet[Categoria]:
        return Categoria.objects.all()

    def buscar_por_slug(self, slug: str) -> Categoria | None:
        return Categoria.objects.filter(slug=slug).first()


class ServicoRepository:
    """Acesso a dados da entidade Servico."""

    def listar_ativos(self) -> QuerySet[Servico]:
        return Servico.objects.filter(ativo=True).select_related("categoria")

    def buscar_por_categoria(self, categoria_slug: str) -> QuerySet[Servico]:
        return self.listar_ativos().filter(categoria__slug=categoria_slug)

    def buscar_por_tipo(self, tipo_sigla: str) -> QuerySet[Servico]:
        return self.listar_ativos().filter(tipo_sigla__iexact=tipo_sigla)

    def buscar_por_termo(self, termo: str) -> QuerySet[Servico]:
        return self.listar_ativos().filter(
            Q(nome__icontains=termo)
            | Q(bairro__icontains=termo)
            | Q(tags__icontains=termo)
            | Q(tipo_sigla__icontains=termo)
        )
