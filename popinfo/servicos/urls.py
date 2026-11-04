from django.urls import path

from .views import ServicoListView, ServicoDetailView

app_name = "servicos"

urlpatterns = [
    path("", ServicoListView.as_view(), name="lista"),
    path('<int:pk>/', ServicoDetailView.as_view(), name='servico_detail'), # <-- Adicione esta linha
]
