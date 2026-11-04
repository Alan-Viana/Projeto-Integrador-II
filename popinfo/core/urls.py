from django.urls import path

from .views import ContatoView, HomeView, SobreView, MapaUnidadesView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("contato/", ContatoView.as_view(), name="contato"),
    path("mapa/", MapaUnidadesView.as_view(), name="mapa"),
]
