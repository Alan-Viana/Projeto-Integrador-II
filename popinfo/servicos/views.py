"""
Camada de Controller (Views) da aplicação Serviços.

As views são propositalmente "magras": recebem a requisição, delegam o
trabalho para a camada de Service e apenas preparam o contexto para o
template. Nenhuma regra de negócio ou consulta ao banco de dados deve
existir diretamente aqui.
"""
from django.shortcuts import render
from django.views import View

from .services import CategoriaService, ServicoService, UnidadeService


class UnidadeListView(View):
    """Exibe a listagem pública das unidades de atendimento, com filtros."""

    template_name = "servicos/lista.html"

    def get(self, request):
        categoria_slug = request.GET.get("categoria")
        sigla_selecionada = request.GET.get("tipo", "todos")
        termo_busca = request.GET.get("q", "").strip()

        context = {
            "unidades": UnidadeService().listar_para_exibicao(
                categoria_slug=categoria_slug,
                sigla=sigla_selecionada,
                termo=termo_busca or None,
            ),
            "categorias": CategoriaService().listar_categorias(),
            "tipos_servico": ServicoService().listar_siglas_para_filtro(),
            "tipo_selecionado": sigla_selecionada,
            "termo_busca": termo_busca,
        }
        return render(request, self.template_name, context)


class UnidadeDetailView(View):
    """Exibe os detalhes de uma unidade junto com seu mapa individual."""

    template_name = "servicos/unidade_detail.html"

    def get(self, request, pk):
        context = {"unidade": UnidadeService().obter_detalhe(pk)}
        return render(request, self.template_name, context)
