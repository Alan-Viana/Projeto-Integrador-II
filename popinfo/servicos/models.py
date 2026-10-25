"""
Camada de Entidade (Entity) da aplicação Serviços.

As classes deste módulo representam o modelo de dados persistido no
banco de dados e não devem conter regras de negócio — apenas estrutura
e validações básicas de campo. Regras de negócio pertencem à camada de
Service (services.py); o acesso a dados é intermediado pela camada de
Repository (repositories.py).
"""
from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    """Representa uma categoria de serviço socioassistencial (ex.: CAPS, Saúde)."""

    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    descricao = models.CharField(
        max_length=255,
        help_text="Descrição curta exibida no card da categoria.",
    )
    icone = models.CharField(
        max_length=50,
        default="bi-heart-pulse",
        help_text="Classe de ícone do Bootstrap Icons, ex.: bi-heart-pulse.",
    )
    ordem = models.PositiveSmallIntegerField(
        default=0,
        help_text="Define a ordem de exibição na página inicial.",
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["ordem", "nome"]

    def __str__(self) -> str:
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Servico(models.Model):
    """Representa um serviço socioassistencial cadastrado na plataforma."""

    class Disponibilidade(models.TextChoices):
        HORARIO_COMERCIAL = "HC", "Horário comercial"
        VINTE_QUATRO_HORAS = "24H", "24 horas"

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="servicos",
    )
    tipo_sigla = models.CharField(
        max_length=30,
        help_text="Sigla/etiqueta exibida no topo do card, ex.: CAPS, C.A / CTA.",
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100, default="São Paulo")
    horario_funcionamento = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Tags separadas por vírgula, ex.: Alimentação,Banho,Pernoite.",
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome

    def lista_tags(self) -> list[str]:
        """Retorna as tags do serviço como uma lista de strings limpas."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
