"""
API REST (somente leitura) da aplicação Serviços.

Endpoints (JSON):
    GET /api/unidades/?tipo=CRAS&categoria=acolhimento&regiao=SUL&q=termo&pagina=1&por_pagina=24
    GET /api/unidades/<id>/
    GET /api/servicos/

Assim como as demais views, apenas delega à camada de Service.
"""
from dataclasses import asdict

from django.http import JsonResponse
from django.urls import path, reverse
from django.views.decorators.http import require_GET

from .services import ServicoService, UnidadeService

JSON_UTF8 = {"ensure_ascii": False}


def _inteiro(valor, padrao):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return padrao


@require_GET
def unidades_lista(request):
    p = request.GET
    resultado = UnidadeService().pesquisar(
        sigla=p.get("tipo"),
        categoria_slug=p.get("categoria"),
        regiao=p.get("regiao"),
        termo=p.get("q", "").strip(),
        pagina=_inteiro(p.get("pagina"), 1),
        por_pagina=_inteiro(p.get("por_pagina"), 24),
    )
    resultado["resultados"] = [
        {**asdict(u), "url": reverse("servicos:unidade_detail", args=[u.id])}
        for u in resultado["resultados"]
    ]
    return JsonResponse(resultado, json_dumps_params=JSON_UTF8)


@require_GET
def unidade_detalhe(request, pk):
    return JsonResponse(asdict(UnidadeService().obter_detalhe(pk)), json_dumps_params=JSON_UTF8)


@require_GET
def servicos_lista(request):
    return JsonResponse(
        {"resultados": ServicoService().listar_catalogo()}, json_dumps_params=JSON_UTF8
    )


app_name = "api"

urlpatterns = [
    path("unidades/", unidades_lista, name="unidades"),
    path("unidades/<int:pk>/", unidade_detalhe, name="unidade"),
    path("servicos/", servicos_lista, name="servicos"),
]
