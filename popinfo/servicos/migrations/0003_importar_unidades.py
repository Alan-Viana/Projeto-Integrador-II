"""Importa as unidades pesquisadas (servicos/dados/unidades.csv).

Fontes: SMADS (dados abertos, dez/2025), CNES/Ministério da Saúde,
páginas oficiais da SMADS, Bom Prato (SEDS-SP) e Cate (SMDET).
"""
import csv
from decimal import Decimal
from pathlib import Path

from django.db import migrations

CSV = Path(__file__).resolve().parent.parent / "dados" / "unidades.csv"
CAMPOS_TEXTO = [
    "nome", "descricao", "endereco", "bairro", "cep", "subprefeitura", "regiao", "cidade",
    "horario_funcionamento", "telefone", "email", "organizacao_gestora", "fonte",
]


def importar(apps, schema_editor):
    Servico = apps.get_model("servicos", "Servico")
    Unidade = apps.get_model("servicos", "Unidade")
    servicos = {s.sigla: s for s in Servico.objects.all()}

    with open(CSV, encoding="utf-8", newline="") as f:
        unidades = [
            Unidade(
                servico=servicos[linha["servico_sigla"]],
                latitude=Decimal(linha["latitude"]) if linha["latitude"] else None,
                longitude=Decimal(linha["longitude"]) if linha["longitude"] else None,
                ativo=linha["ativo"].strip().upper() == "SIM",
                **{c: linha[c].strip() for c in CAMPOS_TEXTO},
            )
            for linha in csv.DictReader(f)
        ]
    Unidade.objects.bulk_create(unidades, batch_size=500)


def remover(apps, schema_editor):
    apps.get_model("servicos", "Unidade").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("servicos", "0002_dados_iniciais"),
    ]

    operations = [
        migrations.RunPython(importar, remover),
    ]
