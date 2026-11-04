"""
Camada de Service da aplicação Serviços.

Os serviços concentram as regras de negócio da aplicação e orquestram o
uso dos repositórios. As camadas de apresentação (views/controllers)
nunca devem acessar os repositórios diretamente — apenas os serviços.

Este módulo também define ViewModels (DTOs) simples, que desacoplam os
templates da estrutura interna das entidades do banco de dados.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from django.shortcuts import get_object_or_404

from .repositories import CategoriaRepository, ServicoRepository
from .models import Servico


@dataclass(frozen=True)
class CategoriaViewModel:
    """Representação de uma categoria pronta para exibição no template."""

    nome: str
    slug: str
    descricao: str
    icone: str


@dataclass(frozen=True)
class ServicoCardViewModel:
    """Representação de um serviço pronta para exibição em um card."""

    id: int  # <-- Adicionado para permitir o link nos cards
    tipo_sigla: str
    nome: str
    descricao: str
    endereco: str
    bairro_cidade: str
    horario_funcionamento: str
    telefone: str
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ServicoDetailViewModel:
    """Representação completa de um serviço para a página de detalhes com mapa."""

    id: int
    tipo_sigla: str
    nome: str
    descricao: str
    endereco: str
    bairro: str
    cidade: str
    horario_funcionamento: str
    telefone: str
    tags: list[str]
    latitude: float | None
    longitude: float | None
    categoria_nome: str


class CategoriaService:
    """Regras de negócio relacionadas às categorias de serviços."""

    def __init__(self, repository: CategoriaRepository | None = None) -> None:
        self._repository = repository or CategoriaRepository()

    def listar_categorias(self) -> list[CategoriaViewModel]:
        return [
            CategoriaViewModel(
                nome=categoria.nome,
                slug=categoria.slug,
                descricao=categoria.descricao,
                icone=categoria.icone,
            )
            for categoria in self._repository.listar_todas()
        ]


class ServicoService:
    """Regras de negócio relacionadas aos serviços socioassistenciais."""

    def __init__(self, repository: ServicoRepository | None = None) -> None:
        self._repository = repository or ServicoRepository()

    def listar_para_exibicao(
        self,
        categoria_slug: str | None = None,
        tipo: str | None = None,
        termo: str | None = None,
    ) -> list[ServicoCardViewModel]:
        """Retorna os serviços a serem exibidos, aplicando filtros opcionais.

        A prioridade de aplicação dos filtros é: termo de busca livre >
        categoria (usada pelos cards da página inicial) > tipo (usado
        pelos filtros rápidos da página de Serviços) > todos os ativos.
        """
        if termo:
            servicos = self._repository.buscar_por_termo(termo)
        elif categoria_slug and categoria_slug != "todos":
            servicos = self._repository.buscar_por_categoria(categoria_slug)
        elif tipo and tipo != "todos":
            servicos = self._repository.buscar_por_tipo(tipo)
        else:
            servicos = self._repository.listar_ativos()

        return [self._para_view_model(servico) for servico in servicos]

    def obter_por_id_para_exibicao(self, servico_id: int) -> ServicoDetailViewModel:
        """Busca um serviço específico pelo ID para a página de detalhes com mapa."""
        servico = get_object_or_404(Servico, pk=servico_id)

        return ServicoDetailViewModel(
            id=servico.id,
            tipo_sigla=servico.tipo_sigla,
            nome=servico.nome,
            descricao=servico.descricao,
            endereco=servico.endereco,
            bairro=servico.bairro,
            cidade=servico.cidade,
            horario_funcionamento=servico.horario_funcionamento,
            telefone=servico.telefone,
            tags=servico.lista_tags(),
            latitude=float(servico.latitude) if servico.latitude else None,
            longitude=float(servico.longitude) if servico.longitude else None,
            categoria_nome=servico.categoria.nome,
        )

    @staticmethod
    def _para_view_model(servico) -> ServicoCardViewModel:
        return ServicoCardViewModel(
            id=servico.id,
            tipo_sigla=servico.tipo_sigla,
            nome=servico.nome,
            descricao=servico.descricao,
            endereco=servico.endereco,
            bairro_cidade=f"{servico.bairro}, {servico.cidade}",
            horario_funcionamento=servico.horario_funcionamento,
            telefone=servico.telefone,
            tags=servico.lista_tags(),
        )