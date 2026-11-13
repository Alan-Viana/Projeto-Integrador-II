from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("painel/", RedirectView.as_view(pattern_name="accounts:painel_unidades"), name="painel"),
    path("painel/unidades/", views.UnidadePainelListView.as_view(), name="painel_unidades"),
    path("painel/unidades/nova/", views.UnidadeCreateView.as_view(), name="unidade_criar"),
    path("painel/unidades/<int:pk>/editar/", views.UnidadeUpdateView.as_view(), name="unidade_editar"),
    path("painel/unidades/<int:pk>/excluir/", views.UnidadeDeleteView.as_view(), name="unidade_excluir"),
    path("painel/usuarios/", views.UsuarioPainelView.as_view(), name="painel_usuarios"),
    path("painel/mensagens/", views.MensagemPainelView.as_view(), name="painel_mensagens"),
]
