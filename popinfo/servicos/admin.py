from django.contrib import admin

from .models import Categoria, Servico


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug", "ordem")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("ordem", "nome")


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "tipo_sigla", "bairro", "ativo")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome", "bairro", "tags")
