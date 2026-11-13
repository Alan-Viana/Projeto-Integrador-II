"""
Camada de Entidade (Entity) da aplicação Serviços.

As classes deste módulo representam o modelo de dados persistido no
banco de dados e não devem conter regras de negócio — apenas estrutura
e validações básicas de campo. Regras de negócio pertencem à camada de
Service (services.py); o acesso a dados é intermediado pela camada de
Repository (repositories.py).

Modelo conceitual
-----------------

    Categoria 1 ── N Servico 1 ── N Acao
                         │
                         1
                         │
                         N
                      Unidade

- Categoria: agrupamento exibido na página inicial (ex.: Acolhimento).
- Servico:   TIPO de serviço, conforme a Tipificação Nacional dos
             Serviços Socioassistenciais (ex.: CRAS, CREAS, Centro POP).
             Concentra as informações comuns a todas as unidades do tipo
             (o que é, para quem é, como acessar, documentos exigidos).
- Acao:      ofertas/atividades realizadas por um tipo de serviço
             (ex.: Pernoite, Banho, Cadastro Único). Substitui o antigo
             campo de "tags" em texto livre.
- Unidade:   local físico de atendimento (endereço, telefone, horário,
             coordenadas para o mapa). É o que o cidadão procura.
"""
from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    """Agrupamento de serviços exibido na página inicial (ex.: CAPS, Saúde)."""

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
    """Tipo de serviço socioassistencial (ex.: CRAS, CREAS, CTA)."""

    class NivelProtecao(models.TextChoices):
        """Níveis de proteção do SUAS (Tipificação Nacional — Res. CNAS 109/2009)."""

        BASICA = "PSB", "Proteção Social Básica"
        ESPECIAL_MEDIA = "PSE-MC", "Proteção Social Especial de Média Complexidade"
        ESPECIAL_ALTA = "PSE-AC", "Proteção Social Especial de Alta Complexidade"
        NAO_SE_APLICA = "NA", "Não se aplica (outras políticas públicas)"

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="servicos",
    )
    sigla = models.CharField(
        max_length=30,
        unique=True,
        help_text="Sigla exibida no card e nos filtros, ex.: CRAS, CREAS, CTA.",
    )
    nome = models.CharField(
        max_length=150,
        help_text="Nome por extenso, ex.: Centro de Referência de Assistência Social.",
    )
    descricao = models.TextField(help_text="O que é o serviço e o que ele oferece.")
    nivel_protecao = models.CharField(
        "nível de proteção",
        max_length=10,
        choices=NivelProtecao.choices,
        default=NivelProtecao.NAO_SE_APLICA,
    )
    publico_alvo = models.CharField(
        "público-alvo",
        max_length=255,
        blank=True,
        help_text="Ex.: Pessoas adultas em situação de rua.",
    )
    como_acessar = models.TextField(
        blank=True,
        help_text="Forma de acesso: demanda espontânea, encaminhamento, agendamento etc.",
    )
    documentos_necessarios = models.CharField(
        "documentos necessários",
        max_length=255,
        blank=True,
        help_text="Ex.: Documento com foto, CPF, comprovante de endereço.",
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["sigla"]

    def __str__(self) -> str:
        return f"{self.sigla} — {self.nome}"


class Acao(models.Model):
    """Oferta/atividade realizada por um tipo de serviço (ex.: Pernoite)."""

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name="acoes",
    )
    nome = models.CharField(max_length=80)
    descricao = models.CharField(max_length=255, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ação"
        verbose_name_plural = "Ações"
        ordering = ["nome"]
        constraints = [
            models.UniqueConstraint(
                fields=["servico", "nome"], name="acao_unica_por_servico"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.nome} ({self.servico.sigla})"


class Unidade(models.Model):
    """Local físico onde um serviço é prestado à população."""

    class Regiao(models.TextChoices):
        CENTRO = "CENTRO", "Centro"
        NORTE = "NORTE", "Norte"
        SUL = "SUL", "Sul"
        LESTE = "LESTE", "Leste"
        OESTE = "OESTE", "Oeste"

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="unidades",
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField(
        blank=True,
        help_text="Informações específicas desta unidade (opcional).",
    )

    # Localização
    endereco = models.CharField(
        "endereço",
        max_length=200,
        help_text="Logradouro e número, ex.: Rua Exemplo, 123.",
    )
    bairro = models.CharField(max_length=100)
    cep = models.CharField("CEP", max_length=9, blank=True)
    subprefeitura = models.CharField(max_length=100, blank=True)
    regiao = models.CharField(
        "região", max_length=10, choices=Regiao.choices, blank=True
    )
    cidade = models.CharField(max_length=100, default="São Paulo")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        help_text="Latitude do endereço para exibição no mapa.",
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        help_text="Longitude do endereço para exibição no mapa.",
    )

    # Atendimento
    horario_funcionamento = models.CharField(
        "horário de funcionamento", max_length=255, blank=True
    )
    telefone = models.CharField(
        max_length=80, blank=True, help_text="Um ou mais números separados por ' / '."
    )
    email = models.EmailField("e-mail", blank=True)
    organizacao_gestora = models.CharField(
        "organização gestora",
        max_length=150,
        blank=True,
        help_text="Órgão público ou OSC parceira que executa o serviço.",
    )

    # Qualidade/rastreabilidade do dado
    fonte = models.URLField(
        max_length=300, blank=True, help_text="Endereço de onde o dado foi obtido."
    )
    verificado_em = models.DateField(
        null=True, blank=True, help_text="Data da última conferência do dado."
    )

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome

    @property
    def possui_coordenadas(self) -> bool:
        return self.latitude is not None and self.longitude is not None
