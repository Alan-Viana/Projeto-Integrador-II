from django.contrib import admin

from .models import Acao, Categoria, Servico, Unidade


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "slug", "ordem")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("ordem", "nome")


class AcaoInline(admin.TabularInline):
    model = Acao
    extra = 1


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("sigla", "nome", "categoria", "nivel_protecao", "ativo")
    list_filter = ("categoria", "nivel_protecao", "ativo")
    search_fields = ("sigla", "nome")
    inlines = [AcaoInline]


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "servico", "bairro", "regiao", "ativo", "verificado_em")
    list_filter = ("servico", "regiao", "ativo")
    search_fields = ("nome", "bairro", "subprefeitura", "endereco")
    list_select_related = ("servico",)
    fieldsets = (
        (None, {"fields": ("servico", "nome", "descricao", "ativo")}),
        ("Localização", {"fields": (
            "endereco", "bairro", "cep", "subprefeitura", "regiao", "cidade",
            "latitude", "longitude",
        )}),
        ("Atendimento", {"fields": (
            "horario_funcionamento", "telefone", "email", "organizacao_gestora",
        )}),
        ("Origem do dado", {"fields": ("fonte", "verificado_em")}),
    )
