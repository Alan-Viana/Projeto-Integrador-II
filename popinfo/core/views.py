"""
Camada de Controller (Views) da aplicação principal.

Início e Categorias são renderizados na mesma página (home.html), com
navegação por rolagem, conforme especificação do projeto.
"""
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from dataclasses import asdict

from servicos.services import CategoriaService, UnidadeService

from .forms import ContatoForm
from .services import ContatoService


class HomeView(View):
    """Página inicial: seção 'Início' (hero + busca) e 'Categorias'."""

    template_name = "core/home.html"

    def get(self, request):
        categoria_service = CategoriaService()
        context = {
            "categorias": categoria_service.listar_categorias(),
        }
        return render(request, self.template_name, context)


class SobreView(View):
    """Página institucional 'Sobre o PopInfo'."""

    template_name = "core/sobre.html"

    def get(self, request):
        return render(request, self.template_name)


class ContatoView(View):
    """Página 'Contato', com formulário de envio de mensagem."""

    template_name = "core/contato.html"

    def get(self, request):
        form = ContatoForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ContatoForm(request.POST)
        if form.is_valid():
            ContatoService().processar_mensagem(form)
            messages.success(
                request,
                "Mensagem enviada com sucesso! Responderemos o quanto antes.",
            )
            return redirect("core:contato")

        messages.error(request, "Verifique os campos destacados e tente novamente.")
        return render(request, self.template_name, {"form": form})


class MapaUnidadesView(View):
    """Página com o mapa de unidades e sistema de geolocalização dual."""

    template_name = "core/mapa.html"

    def get(self, request):
        unidades = [asdict(u) for u in UnidadeService().listar_para_mapa()]
        return render(request, self.template_name, {"unidades": unidades})
