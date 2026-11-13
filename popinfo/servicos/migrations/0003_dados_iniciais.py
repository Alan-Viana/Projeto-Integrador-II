"""
Dados de referência (domínio) da aplicação: categorias e tipos de serviço.

Estes dados não mudam com frequência e descrevem O QUE é cada serviço,
com base na Tipificação Nacional dos Serviços Socioassistenciais
(Resolução CNAS nº 109/2009) e na rede da Secretaria Municipal de
Assistência e Desenvolvimento Social (SMADS) de São Paulo.

As UNIDADES (endereços reais) não são criadas aqui: elas são carregadas
a partir da planilha de dados pesquisados.
"""
from django.db import migrations

CATEGORIAS = [
    ("CAPS", "caps", "Centros de Atenção Psicossocial para saúde mental e dependência química.", "bi-clipboard2-pulse", 1),
    ("Acolhimento", "acolhimento", "Serviços de acolhimento e moradia temporária.", "bi-house-heart", 2),
    ("Saúde", "saude", "Atendimento médico, consultas e serviços de saúde pública.", "bi-heart-pulse", 3),
    ("Alimentação", "alimentacao", "Restaurantes populares, cestas básicas e bancos de alimentos.", "bi-basket2", 4),
    ("Rede Socioassistencial", "rede-socioassistencial", "CRAS, CREAS e outros serviços de proteção social.", "bi-diagram-3", 5),
    ("Emprego", "emprego", "Capacitação profissional e oportunidades de trabalho.", "bi-briefcase", 6),
]

DOC_BASICO = "Documento de identificação com foto e CPF (se não tiver, a unidade orienta como emitir)."

# (categoria_slug, sigla, nome, nivel, publico_alvo, descricao, como_acessar, documentos, [acoes])
SERVICOS = [
    (
        "rede-socioassistencial", "CRAS", "Centro de Referência de Assistência Social", "PSB",
        "Famílias e pessoas em situação de vulnerabilidade social.",
        "Porta de entrada da assistência social. Oferece acompanhamento a famílias (PAIF), "
        "inclusão no Cadastro Único, orientação sobre benefícios sociais e encaminhamento "
        "para a rede de serviços.",
        "Procure a unidade mais próxima da sua residência (demanda espontânea) ou ligue para agendar.",
        DOC_BASICO + " Comprovante de endereço, se tiver.",
        ["Cadastro Único", "Acompanhamento familiar (PAIF)", "Orientação sobre benefícios", "Encaminhamentos"],
    ),
    (
        "rede-socioassistencial", "CREAS", "Centro de Referência Especializado de Assistência Social", "PSE-MC",
        "Famílias e pessoas com direitos violados (violência, abandono, exploração, discriminação).",
        "Atendimento especializado a famílias e indivíduos em situação de violação de direitos, "
        "por meio do PAEFI, além do acompanhamento de adolescentes em medidas socioeducativas "
        "em meio aberto.",
        "Demanda espontânea ou encaminhamento do CRAS, Conselho Tutelar, Judiciário ou rede de saúde.",
        DOC_BASICO,
        ["Atendimento a violação de direitos (PAEFI)", "Medidas socioeducativas", "Orientação jurídico-social"],
    ),
    (
        "rede-socioassistencial", "Centro POP", "Centro de Referência Especializado para População em Situação de Rua", "PSE-MC",
        "Pessoas em situação de rua.",
        "Espaço de referência durante o dia para pessoas em situação de rua, com atendimento "
        "social, higiene pessoal, guarda de pertences e endereço de referência para documentos.",
        "Demanda espontânea: basta comparecer à unidade no horário de funcionamento.",
        "Não é exigido documento para o primeiro atendimento.",
        ["Banho", "Lavagem de roupas", "Guarda de pertences", "Endereço de referência", "Atendimento social"],
    ),
    (
        "acolhimento", "CA", "Centro de Acolhida para Adultos", "PSE-AC",
        "Pessoas adultas em situação de rua (há unidades específicas para mulheres, famílias e idosos).",
        "Acolhimento institucional com pernoite, alimentação e acompanhamento social, "
        "visando a construção da saída da situação de rua.",
        "Encaminhamento pela CAPE (telefone 156), pelo Centro POP ou pelas equipes de abordagem social.",
        "Não é exigido documento para o acolhimento.",
        ["Pernoite", "Alimentação", "Banho", "Acompanhamento social"],
    ),
    (
        "rede-socioassistencial", "NCI", "Núcleo de Convivência de Idosos", "PSB",
        "Pessoas idosas (60 anos ou mais).",
        "Atividades de convivência e fortalecimento de vínculos para pessoas idosas, "
        "prevenindo o isolamento social.",
        "Procure a unidade ou o CRAS da sua região.",
        DOC_BASICO,
        ["Atividades de convivência", "Oficinas", "Atividades físicas e culturais"],
    ),
    (
        "rede-socioassistencial", "CCA", "Centro para Crianças e Adolescentes", "PSB",
        "Crianças e adolescentes de 6 a 14 anos e 11 meses.",
        "Serviço de convivência e fortalecimento de vínculos no contraturno escolar, com "
        "atividades socioeducativas, culturais e esportivas.",
        "Inscrição pelo CRAS da região ou diretamente na unidade, conforme disponibilidade de vagas.",
        "Certidão de nascimento ou RG da criança, documento do responsável e comprovante de endereço.",
        ["Contraturno escolar", "Atividades culturais e esportivas", "Alimentação"],
    ),
    (
        "caps", "CAPS", "Centro de Atenção Psicossocial", "NA",
        "Pessoas com sofrimento mental grave ou problemas decorrentes do uso de álcool e outras drogas.",
        "Serviço de saúde mental do SUS. Há modalidades Adulto, Infantojuvenil (IJ) e "
        "Álcool e Drogas (AD), algumas com funcionamento 24 horas.",
        "Demanda espontânea (sem necessidade de encaminhamento) ou encaminhamento da UBS.",
        "Cartão SUS e documento com foto (se não tiver, a unidade orienta).",
        ["Acolhimento em saúde mental", "Atendimento psicológico e psiquiátrico", "Atividades terapêuticas"],
    ),
    (
        "saude", "UBS", "Unidade Básica de Saúde", "NA",
        "Toda a população, conforme território de residência.",
        "Porta de entrada do SUS: consultas, vacinação, curativos, exames e acompanhamento "
        "pelas equipes de Saúde da Família.",
        "Procure a UBS de referência do seu endereço. Pessoas em situação de rua são atendidas "
        "em qualquer UBS ou pelas equipes do Consultório na Rua.",
        "Cartão SUS e documento com foto (o atendimento não pode ser negado por falta de documento).",
        ["Consultas", "Vacinação", "Exames", "Saúde da Família"],
    ),
    (
        "alimentacao", "Bom Prato", "Restaurante Bom Prato", "NA",
        "Toda a população, prioritariamente pessoas em vulnerabilidade.",
        "Restaurantes populares do Governo do Estado de São Paulo, com refeições "
        "balanceadas a preço reduzido (pessoas em situação de rua podem ter gratuidade).",
        "Basta comparecer à unidade no horário de funcionamento.",
        "Nenhum documento é exigido.",
        ["Café da manhã", "Almoço", "Jantar (em algumas unidades)"],
    ),
    (
        "emprego", "Cate", "Centro de Apoio ao Trabalho e Empreendedorismo", "NA",
        "Pessoas em busca de emprego, qualificação ou apoio para empreender.",
        "Unidades da Prefeitura de São Paulo que oferecem intermediação de vagas de emprego, "
        "orientação para o seguro-desemprego, qualificação profissional e apoio ao "
        "empreendedor (MEI).",
        "Atendimento presencial nas unidades; alguns serviços exigem agendamento prévio.",
        "Documento com foto, CPF e Carteira de Trabalho (física ou digital).",
        ["Vagas de emprego", "Seguro-desemprego", "Qualificação profissional", "Apoio ao MEI"],
    ),
]


def criar_dados_iniciais(apps, schema_editor):
    Categoria = apps.get_model("servicos", "Categoria")
    Servico = apps.get_model("servicos", "Servico")
    Acao = apps.get_model("servicos", "Acao")

    categorias = {}
    for nome, slug, descricao, icone, ordem in CATEGORIAS:
        categorias[slug], _ = Categoria.objects.get_or_create(
            slug=slug,
            defaults={"nome": nome, "descricao": descricao, "icone": icone, "ordem": ordem},
        )

    for (cat_slug, sigla, nome, nivel, publico, descricao,
         como_acessar, documentos, acoes) in SERVICOS:
        servico, _ = Servico.objects.get_or_create(
            sigla=sigla,
            defaults={
                "categoria": categorias[cat_slug],
                "nome": nome,
                "nivel_protecao": nivel,
                "publico_alvo": publico,
                "descricao": descricao,
                "como_acessar": como_acessar,
                "documentos_necessarios": documentos,
            },
        )
        for nome_acao in acoes:
            Acao.objects.get_or_create(servico=servico, nome=nome_acao)


def remover_dados_iniciais(apps, schema_editor):
    Categoria = apps.get_model("servicos", "Categoria")
    Servico = apps.get_model("servicos", "Servico")
    Servico.objects.filter(sigla__in=[s[1] for s in SERVICOS]).delete()
    Categoria.objects.filter(slug__in=[c[1] for c in CATEGORIAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("servicos", "0002c_remove_legacy_tipo_sigla"),
    ]

    operations = [
        migrations.RunPython(criar_dados_iniciais, remover_dados_iniciais),
    ]
