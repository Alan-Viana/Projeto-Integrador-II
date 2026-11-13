from django.urls import path

from .views import UnidadeDetailView, UnidadeListView

app_name = "servicos"

urlpatterns = [
    path("", UnidadeListView.as_view(), name="lista"),
    path("<int:pk>/", UnidadeDetailView.as_view(), name="unidade_detail"),
]
