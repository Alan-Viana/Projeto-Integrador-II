"""
Camada de Controller (Views) da aplicação Serviços.

As views são propositalmente "magras": recebem a requisição, delegam o
trabalho para a camada de Service e apenas preparam o contexto para o
template. Nenhuma regra de negócio ou consulta ao banco de dados deve
existir diretamente aqui.
"""
from django.shortcuts import render
from django.views import View

from .models import Unidade
from .services import CategoriaService, ServicoService, UnidadeService


class UnidadeListView(View):
    """Exibe a listagem pública das unidades de atendimento, com filtros."""

    template_name = "servicos/lista.html"

    def get(self, request):
        p = request.GET
        categoria_slug = p.get("categoria", "")
        sigla_selecionada = p.get("tipo", "todos")
        regiao = p.get("regiao", "")
        termo_busca = p.get("q", "").strip()

        resultado = UnidadeService().pesquisar(
            sigla=sigla_selecionada,
            categoria_slug=categoria_slug,
            regiao=regiao,
            termo=termo_busca,
            pagina=p.get("pagina") or 1,
        )
        context = {
            "unidades": resultado["resultados"],
            "total": resultado["total"],
            "pagina": resultado["pagina"],
            "paginas": resultado["paginas"],
            "categorias": CategoriaService().listar_categorias(),
            "tipos_servico": ServicoService().listar_siglas_para_filtro(),
            "regioes": Unidade.Regiao.choices,
            "tipo_selecionado": sigla_selecionada,
            "categoria_selecionada": categoria_slug,
            "regiao_selecionada": regiao,
            "termo_busca": termo_busca,
        }
        return render(request, self.template_name, context)


class UnidadeDetailView(View):
    """Exibe os detalhes de uma unidade junto com seu mapa individual."""

    template_name = "servicos/unidade_detail.html"

    def get(self, request, pk):
        context = {"unidade": UnidadeService().obter_detalhe(pk)}
        return render(request, self.template_name, context)
