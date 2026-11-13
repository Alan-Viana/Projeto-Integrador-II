"""
Camada de Repository da aplicação Serviços.

Os repositórios isolam toda a interação com o ORM do Django (consultas ao
banco de dados). Nenhuma outra camada da aplicação deve importar os
modelos diretamente para fazer consultas — apenas os repositórios têm
essa responsabilidade. Isso facilita testes (é possível substituir o
repositório por um "fake" em memória) e futuras trocas de fonte de dados.
"""
from __future__ import annotations

from django.db.models import Prefetch, Q, QuerySet

from .models import Acao, Categoria, Servico, Unidade


class CategoriaRepository:
    """Acesso a dados da entidade Categoria."""

    def listar_todas(self) -> QuerySet[Categoria]:
        return Categoria.objects.all()

    def buscar_por_slug(self, slug: str) -> Categoria | None:
        return Categoria.objects.filter(slug=slug).first()


class ServicoRepository:
    """Acesso a dados da entidade Servico (tipos de serviço)."""

    def listar_ativos(self) -> QuerySet[Servico]:
        return Servico.objects.filter(ativo=True).select_related("categoria")

    def listar_siglas_com_unidades(self) -> list[str]:
        """Siglas dos serviços que possuem ao menos uma unidade ativa."""
        return list(
            self.listar_ativos()
            .filter(unidades__ativo=True)
            .values_list("sigla", flat=True)
            .distinct()
            .order_by("sigla")
        )


class UnidadeRepository:
    """Acesso a dados da entidade Unidade (locais de atendimento)."""

    def listar_ativas(self) -> QuerySet[Unidade]:
        acoes_ativas = Prefetch(
            "servico__acoes", queryset=Acao.objects.filter(ativo=True)
        )
        return (
            Unidade.objects.filter(ativo=True, servico__ativo=True)
            .select_related("servico", "servico__categoria")
            .prefetch_related(acoes_ativas)
        )

    def buscar_por_id(self, unidade_id: int) -> Unidade | None:
        return self.listar_ativas().filter(pk=unidade_id).first()

    def buscar_por_categoria(self, categoria_slug: str) -> QuerySet[Unidade]:
        return self.listar_ativas().filter(servico__categoria__slug=categoria_slug)

    def buscar_por_sigla(self, sigla: str) -> QuerySet[Unidade]:
        return self.listar_ativas().filter(servico__sigla__iexact=sigla)

    def buscar_por_termo(self, termo: str) -> QuerySet[Unidade]:
        return self.listar_ativas().filter(
            Q(nome__icontains=termo)
            | Q(bairro__icontains=termo)
            | Q(subprefeitura__icontains=termo)
            | Q(servico__sigla__icontains=termo)
            | Q(servico__nome__icontains=termo)
            | Q(servico__categoria__nome__icontains=termo)
            | Q(servico__acoes__nome__icontains=termo)
        ).distinct()

    def listar_com_coordenadas(self) -> QuerySet[Unidade]:
        return self.listar_ativas().filter(
            latitude__isnull=False, longitude__isnull=False
        )
