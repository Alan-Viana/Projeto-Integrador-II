from django.db import migrations


CATEGORIAS = [
    {
        "nome": "CAPS",
        "slug": "caps",
        "descricao": "Centros de Atenção Psicossocial para saúde mental e dependência química.",
        "icone": "bi-clipboard2-pulse",
        "ordem": 1,
    },
    {
        "nome": "Acolhimento",
        "slug": "acolhimento",
        "descricao": "Serviços de acolhimento e moradia temporária.",
        "icone": "bi-house-heart",
        "ordem": 2,
    },
    {
        "nome": "Saúde",
        "slug": "saude",
        "descricao": "Atendimento médico, consultas e serviços de saúde pública.",
        "icone": "bi-heart-pulse",
        "ordem": 3,
    },
    {
        "nome": "Alimentação",
        "slug": "alimentacao",
        "descricao": "Restaurantes populares, cestas básicas e bancos de alimentos.",
        "icone": "bi-basket2",
        "ordem": 4,
    },
    {
        "nome": "Rede Socioassistencial",
        "slug": "rede-socioassistencial",
        "descricao": "CRAS, CREAS e outros serviços de proteção social básica.",
        "icone": "bi-diagram-3",
        "ordem": 5,
    },
    {
        "nome": "Emprego",
        "slug": "emprego",
        "descricao": "Capacitação profissional e oportunidades de trabalho.",
        "icone": "bi-briefcase",
        "ordem": 6,
    },
]

SERVICO_EXEMPLO = {
    "categoria_slug": "acolhimento",
    "tipo_sigla": "C.A / CTA",
    "nome": "Centro Temporário De Acolhimento Vila Mariana",
    "descricao": (
        "Os Centros Temporários de Acolhimento (CTA) são serviços "
        "socioassistenciais da Prefeitura de São Paulo, criados para "
        "oferecer abrigo provisório de rápida permanência a pessoas em "
        "situação de rua, garantindo alimentação, higiene pessoal e "
        "descanso seguro."
    ),
    "endereco": "Avenida José Maria Whitaker, 2000",
    "bairro": "Planalto Paulista",
    "cidade": "São Paulo",
    "horario_funcionamento": "24 horas",
    "telefone": "(11) 5078-0555",
    "tags": "Alimentação,Banho,Pernoite",
    "ativo": True,
}


def criar_dados_exemplo(apps, schema_editor):
    Categoria = apps.get_model("servicos", "Categoria")
    Servico = apps.get_model("servicos", "Servico")

    slug_para_categoria = {}
    for dados_categoria in CATEGORIAS:
        categoria, _ = Categoria.objects.get_or_create(
            slug=dados_categoria["slug"],
            defaults=dados_categoria,
        )
        slug_para_categoria[dados_categoria["slug"]] = categoria

    categoria_do_exemplo = slug_para_categoria[SERVICO_EXEMPLO["categoria_slug"]]
    Servico.objects.get_or_create(
        nome=SERVICO_EXEMPLO["nome"],
        defaults={
            "categoria": categoria_do_exemplo,
            "tipo_sigla": SERVICO_EXEMPLO["tipo_sigla"],
            "descricao": SERVICO_EXEMPLO["descricao"],
            "endereco": SERVICO_EXEMPLO["endereco"],
            "bairro": SERVICO_EXEMPLO["bairro"],
            "cidade": SERVICO_EXEMPLO["cidade"],
            "horario_funcionamento": SERVICO_EXEMPLO["horario_funcionamento"],
            "telefone": SERVICO_EXEMPLO["telefone"],
            "tags": SERVICO_EXEMPLO["tags"],
            "ativo": SERVICO_EXEMPLO["ativo"],
        },
    )


def remover_dados_exemplo(apps, schema_editor):
    Categoria = apps.get_model("servicos", "Categoria")
    Servico = apps.get_model("servicos", "Servico")
    Servico.objects.filter(nome=SERVICO_EXEMPLO["nome"]).delete()
    Categoria.objects.filter(slug__in=[c["slug"] for c in CATEGORIAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("servicos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(criar_dados_exemplo, remover_dados_exemplo),
    ]
