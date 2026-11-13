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

from django.core.paginator import Paginator
from django.http import Http404

from .models import Unidade
from .repositories import CategoriaRepository, ServicoRepository, UnidadeRepository


@dataclass(frozen=True)
class CategoriaViewModel:
    """Representação de uma categoria pronta para exibição no template."""

    nome: str
    slug: str
    descricao: str
    icone: str


@dataclass(frozen=True)
class UnidadeCardViewModel:
    """Representação de uma unidade pronta para exibição em um card."""

    id: int
    sigla: str
    nome: str
    descricao: str
    endereco: str
    bairro_cidade: str
    horario_funcionamento: str
    telefone: str
    acoes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class UnidadeDetailViewModel:
    """Representação completa de uma unidade para a página de detalhes com mapa."""

    id: int
    nome: str
    descricao: str
    endereco: str
    bairro: str
    cep: str
    cidade: str
    subprefeitura: str
    regiao: str
    horario_funcionamento: str
    telefone: str
    email: str
    organizacao_gestora: str
    latitude: float | None
    longitude: float | None
    acoes: list[str]
    # Dados do tipo de serviço
    sigla: str
    servico_nome: str
    nivel_protecao: str
    publico_alvo: str
    como_acessar: str
    documentos_necessarios: str
    categoria_nome: str


@dataclass(frozen=True)
class UnidadeMapaViewModel:
    """Dados mínimos de uma unidade para o marcador no mapa (serializável em JSON)."""

    id: int
    nome: str
    sigla: str
    endereco: str
    latitude: float
    longitude: float


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
    """Regras de negócio relacionadas aos tipos de serviço."""

    def __init__(self, repository: ServicoRepository | None = None) -> None:
        self._repository = repository or ServicoRepository()

    def listar_siglas_para_filtro(self) -> list[str]:
        """Siglas exibidas nos filtros rápidos (apenas as que têm unidades)."""
        return self._repository.listar_siglas_com_unidades()

    def siglas_por_categoria(self, categoria_slug: str) -> list[str]:
        """Retorna todos os chips pertencentes à categoria selecionada."""
        siglas_com_unidades = set(self.listar_siglas_para_filtro())
        siglas_da_categoria = self._repository.listar_ativos().filter(
            categoria__slug=categoria_slug
        ).values_list("sigla", flat=True)
        return [sigla for sigla in siglas_da_categoria if sigla in siglas_com_unidades]

    def listar_catalogo(self) -> list[dict]:
        """Tipos de serviço ativos com suas ações (para a API)."""
        return [
            {
                "sigla": s.sigla,
                "nome": s.nome,
                "categoria": s.categoria.nome,
                "nivel_protecao": s.get_nivel_protecao_display(),
                "publico_alvo": s.publico_alvo,
                "como_acessar": s.como_acessar,
                "documentos_necessarios": s.documentos_necessarios,
                "acoes": [a.nome for a in s.acoes.all() if a.ativo],
            }
            for s in self._repository.listar_ativos().prefetch_related("acoes")
        ]


class UnidadeService:
    """Regras de negócio relacionadas às unidades de atendimento."""

    def __init__(self, repository: UnidadeRepository | None = None) -> None:
        self._repository = repository or UnidadeRepository()

    def listar_para_exibicao(
        self,
        categoria_slug: str | None = None,
        sigla: str | None = None,
        termo: str | None = None,
    ) -> list[UnidadeCardViewModel]:
        """Retorna as unidades a serem exibidas, aplicando filtros opcionais.

        A prioridade de aplicação dos filtros é: termo de busca livre >
        categoria (usada pelos cards da página inicial) > sigla do serviço
        (usada pelos filtros rápidos da página de Serviços) > todas as ativas.
        """
        if termo:
            unidades = self._repository.buscar_por_termo(termo)
        elif categoria_slug and categoria_slug != "todos":
            unidades = self._repository.buscar_por_categoria(categoria_slug)
        elif sigla and sigla != "todos":
            unidades = self._repository.buscar_por_sigla(sigla)
        else:
            unidades = self._repository.listar_ativas()

        return [self._para_card(unidade) for unidade in unidades]

    def pesquisar(
        self,
        sigla: str | None = None,
        categoria_slug: str | None = None,
        regiao: str | None = None,
        termo: str | None = None,
        pagina: int = 1,
        por_pagina: int = 24,
    ) -> dict:
        """Busca paginada com filtros combinados (usada pela API e pela lista)."""
        por_pagina = max(1, min(por_pagina, 100))
        unidades = self._repository.filtrar(
            sigla=None if sigla in (None, "", "todos") else sigla,
            categoria_slug=categoria_slug or None,
            regiao=regiao or None,
            termo=termo or None,
        )
        paginador = Paginator(unidades, por_pagina)
        pagina_atual = paginador.get_page(pagina)
        return {
            "total": paginador.count,
            "pagina": pagina_atual.number,
            "paginas": paginador.num_pages,
            "resultados": [self._para_card(u) for u in pagina_atual.object_list],
        }

    def obter_detalhe(self, unidade_id: int) -> UnidadeDetailViewModel:
        """Busca uma unidade ativa pelo ID; lança Http404 se não existir."""
        unidade = self._repository.buscar_por_id(unidade_id)
        if unidade is None:
            raise Http404("Unidade não encontrada.")

        servico = unidade.servico
        return UnidadeDetailViewModel(
            id=unidade.id,
            nome=unidade.nome,
            descricao=unidade.descricao or servico.descricao,
            endereco=unidade.endereco,
            bairro=unidade.bairro,
            cep=unidade.cep,
            cidade=unidade.cidade,
            subprefeitura=unidade.subprefeitura,
            regiao=unidade.get_regiao_display(),
            horario_funcionamento=unidade.horario_funcionamento,
            telefone=unidade.telefone,
            email=unidade.email,
            organizacao_gestora=unidade.organizacao_gestora,
            latitude=float(unidade.latitude) if unidade.latitude is not None else None,
            longitude=float(unidade.longitude) if unidade.longitude is not None else None,
            acoes=self._nomes_acoes(unidade),
            sigla=servico.sigla,
            servico_nome=servico.nome,
            nivel_protecao=servico.get_nivel_protecao_display(),
            publico_alvo=servico.publico_alvo,
            como_acessar=servico.como_acessar,
            documentos_necessarios=servico.documentos_necessarios,
            categoria_nome=servico.categoria.nome,
        )

    def listar_para_mapa(self) -> list[UnidadeMapaViewModel]:
        """Unidades com coordenadas, prontas para virar marcadores no mapa."""
        return [
            UnidadeMapaViewModel(
                id=unidade.id,
                nome=unidade.nome,
                sigla=unidade.servico.sigla,
                endereco=f"{unidade.endereco} — {unidade.bairro}",
                latitude=float(unidade.latitude),
                longitude=float(unidade.longitude),
            )
            for unidade in self._repository.listar_com_coordenadas()
        ]

    @staticmethod
    def _nomes_acoes(unidade: Unidade) -> list[str]:
        # Usa o prefetch feito no repositório (sem nova consulta ao banco).
        return [acao.nome for acao in unidade.servico.acoes.all()]

    @classmethod
    def _para_card(cls, unidade: Unidade) -> UnidadeCardViewModel:
        return UnidadeCardViewModel(
            id=unidade.id,
            sigla=unidade.servico.sigla,
            nome=cls._nome_sem_endereco(unidade.nome),
            descricao=unidade.descricao or unidade.servico.descricao,
            endereco=unidade.endereco,
            bairro_cidade=f"{unidade.bairro}, {unidade.cidade}",
            horario_funcionamento=unidade.horario_funcionamento,
            telefone=unidade.telefone,
            acoes=cls._nomes_acoes(unidade),
        )

    @staticmethod
    def _nome_sem_endereco(nome: str) -> str:
        """Mantém no título do card apenas o nome da unidade."""
        return nome.split(" — ", 1)[0].strip()
