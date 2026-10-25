"""
Camada de Controller (Views) da aplicação Serviços.

As views são propositalmente "magras": recebem a requisição, delegam o
trabalho para a camada de Service e apenas preparam o contexto para o
template. Nenhuma regra de negócio ou consulta ao banco de dados deve
existir diretamente aqui.
"""
from django.views import View
from django.shortcuts import render

from .constants import TIPOS_SERVICO
from .services import CategoriaService, ServicoService


class ServicoListView(View):
    """Exibe a listagem pública de serviços socioassistenciais, com filtros."""

    template_name = "servicos/lista.html"

    def get(self, request):
        categoria_slug = request.GET.get("categoria")
        tipo_selecionado = request.GET.get("tipo", "todos")
        termo_busca = request.GET.get("q", "").strip()

        servico_service = ServicoService()
        categoria_service = CategoriaService()

        context = {
            "servicos": servico_service.listar_para_exibicao(
                categoria_slug=categoria_slug,
                tipo=tipo_selecionado,
                termo=termo_busca or None,
            ),
            "categorias": categoria_service.listar_categorias(),
            "tipos_servico": TIPOS_SERVICO,
            "tipo_selecionado": tipo_selecionado,
            "termo_busca": termo_busca,
        }
        return render(request, self.template_name, context)
