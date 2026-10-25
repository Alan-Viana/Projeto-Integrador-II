from django.urls import path

from .views import ServicoListView

app_name = "servicos"

urlpatterns = [
    path("", ServicoListView.as_view(), name="lista"),
]
