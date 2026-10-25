import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=110, unique=True)),
                (
                    "descricao",
                    models.CharField(
                        help_text="Descrição curta exibida no card da categoria.",
                        max_length=255,
                    ),
                ),
                (
                    "icone",
                    models.CharField(
                        default="bi-heart-pulse",
                        help_text="Classe de ícone do Bootstrap Icons, ex.: bi-heart-pulse.",
                        max_length=50,
                    ),
                ),
                (
                    "ordem",
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text="Define a ordem de exibição na página inicial.",
                    ),
                ),
            ],
            options={
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
                "ordering": ["ordem", "nome"],
            },
        ),
        migrations.CreateModel(
            name="Servico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "tipo_sigla",
                    models.CharField(
                        help_text="Sigla/etiqueta exibida no topo do card, ex.: CAPS, C.A / CTA.",
                        max_length=30,
                    ),
                ),
                ("nome", models.CharField(max_length=150)),
                ("descricao", models.TextField()),
                ("endereco", models.CharField(max_length=200)),
                ("bairro", models.CharField(max_length=100)),
                ("cidade", models.CharField(default="São Paulo", max_length=100)),
                ("horario_funcionamento", models.CharField(max_length=100)),
                ("telefone", models.CharField(max_length=20)),
                (
                    "tags",
                    models.CharField(
                        blank=True,
                        help_text="Tags separadas por vírgula, ex.: Alimentação,Banho,Pernoite.",
                        max_length=255,
                    ),
                ),
                ("ativo", models.BooleanField(default=True)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="servicos",
                        to="servicos.categoria",
                    ),
                ),
            ],
            options={
                "verbose_name": "Serviço",
                "verbose_name_plural": "Serviços",
                "ordering": ["nome"],
            },
        ),
    ]
