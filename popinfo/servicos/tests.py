from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from servicos.models import Acao, Categoria, Servico, Unidade
from servicos.services import UnidadeService


def criar_cenario():
    """Cria uma categoria, um tipo de serviço com ações e uma unidade ativa."""
    categoria = Categoria.objects.create(
        nome="Categoria Teste", descricao="Categoria usada nos testes."
    )
    servico = Servico.objects.create(
        categoria=categoria,
        sigla="TESTE",
        nome="Serviço de Teste",
        descricao="Descrição do tipo de serviço.",
        nivel_protecao=Servico.NivelProtecao.BASICA,
    )
    Acao.objects.create(servico=servico, nome="Cadastro Único")
    Acao.objects.create(servico=servico, nome="Ação Inativa", ativo=False)
    unidade = Unidade.objects.create(
        servico=servico,
        nome="Unidade Vila Esperança",
        endereco="Rua das Flores, 500",
        bairro="Vila Esperança",
        regiao=Unidade.Regiao.LESTE,
        latitude=Decimal("-23.540000"),
        longitude=Decimal("-46.480000"),
    )
    return categoria, servico, unidade


class ModelosTestCase(TestCase):
    """Testes unitários das entidades."""

    def test_categoria_gera_slug_automaticamente(self):
        categoria = Categoria.objects.create(nome="Proteção Social Básica", descricao="x")
        self.assertEqual(categoria.slug, "protecao-social-basica")

    def test_criacao_unidade_vinculada_ao_servico(self):
        _, servico, unidade = criar_cenario()
        self.assertIsNotNone(unidade.id)
        self.assertEqual(unidade.servico, servico)
        self.assertEqual(unidade.cidade, "São Paulo")
        self.assertTrue(unidade.possui_coordenadas)

    def test_acao_nao_pode_repetir_no_mesmo_servico(self):
        _, servico, _ = criar_cenario()
        with self.assertRaises(IntegrityError):
            Acao.objects.create(servico=servico, nome="Cadastro Único")

    def test_unidades_importadas_pela_migration(self):
        self.assertEqual(Unidade.objects.count(), 1477)
        self.assertFalse(Unidade.objects.filter(servico__sigla="CTA").exists())

    def test_dados_iniciais_carregados_pela_migration(self):
        self.assertTrue(Servico.objects.filter(sigla="CRAS").exists())
        self.assertTrue(Categoria.objects.filter(slug="acolhimento").exists())


class UnidadeServiceTestCase(TestCase):
    """Testes das regras de negócio da camada de Service."""

    def setUp(self):
        self.categoria, self.servico, self.unidade = criar_cenario()
        self.service = UnidadeService()

    def test_card_exibe_apenas_acoes_ativas(self):
        cards = self.service.listar_para_exibicao(sigla="TESTE")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0].acoes, ["Cadastro Único"])

    def test_descricao_da_unidade_herda_a_do_servico_quando_vazia(self):
        card = self.service.listar_para_exibicao(sigla="TESTE")[0]
        self.assertEqual(card.descricao, self.servico.descricao)

    def test_card_remove_endereco_embutido_no_nome(self):
        self.unidade.nome = "Unidade Vila Esperança — Rua Principal, 100"
        self.unidade.save()

        card = self.service.listar_para_exibicao(sigla="TESTE")[0]

        self.assertEqual(card.nome, "Unidade Vila Esperança")

    def test_busca_por_termo_encontra_pela_acao(self):
        cards = self.service.listar_para_exibicao(termo="cadastro")
        self.assertIn("Unidade Vila Esperança", [c.nome for c in cards])

    def test_filtro_por_categoria(self):
        cards = self.service.listar_para_exibicao(categoria_slug=self.categoria.slug)
        self.assertEqual(len(cards), 1)

    def test_unidade_inativa_nao_e_listada(self):
        self.unidade.ativo = False
        self.unidade.save()
        self.assertEqual(self.service.listar_para_exibicao(sigla="TESTE"), [])

    def test_mapa_ignora_unidades_sem_coordenadas(self):
        Unidade.objects.create(
            servico=self.servico, nome="Sem GPS", endereco="Rua X, 1", bairro="Centro"
        )
        nomes = [u.nome for u in self.service.listar_para_mapa()]
        self.assertIn("Unidade Vila Esperança", nomes)
        self.assertNotIn("Sem GPS", nomes)


class UnidadeIntegrationTestCase(TestCase):
    """Testes de integração: View + Service + Repository + Template."""

    def setUp(self):
        _, _, self.unidade = criar_cenario()

    def test_fluxo_listagem_exibe_dados_no_html(self):
        response = self.client.get(reverse("servicos:lista"), {"tipo": "TESTE"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unidade Vila Esperança")
        self.assertContains(response, "Rua das Flores, 500")
        self.assertContains(response, "TESTE")

    def test_pagina_de_detalhe(self):
        response = self.client.get(reverse("servicos:unidade_detail", args=[self.unidade.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Serviço de Teste")
        self.assertContains(response, "Cadastro Único")

    def test_detalhe_inexistente_retorna_404(self):
        response = self.client.get(reverse("servicos:unidade_detail", args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_pagina_do_mapa_carrega_com_coordenadas(self):
        response = self.client.get(reverse("core:mapa"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "-23.54")


class ApiTestCase(TestCase):
    """Testes da API REST (JSON)."""

    def setUp(self):
        _, _, self.unidade = criar_cenario()

    def test_lista_unidades_filtra_e_pagina(self):
        resposta = self.client.get(reverse("api:unidades"), {"tipo": "TESTE", "por_pagina": 5})
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.json()
        self.assertEqual(dados["total"], 1)
        self.assertEqual(dados["resultados"][0]["nome"], "Unidade Vila Esperança")
        self.assertEqual(dados["resultados"][0]["url"], f"/servicos/{self.unidade.id}/")

    def test_filtros_combinados(self):
        dados = self.client.get(reverse("api:unidades"), {"tipo": "TESTE", "regiao": "SUL"}).json()
        self.assertEqual(dados["total"], 0)

    def test_paginacao_dos_dados_importados(self):
        dados = self.client.get(reverse("api:unidades"), {"tipo": "CRAS", "por_pagina": 10}).json()
        self.assertEqual(dados["total"], 54)
        self.assertEqual(dados["paginas"], 6)
        self.assertEqual(len(dados["resultados"]), 10)

    def test_detalhe_e_404(self):
        self.assertEqual(self.client.get(reverse("api:unidade", args=[self.unidade.id])).json()["sigla"], "TESTE")
        self.assertEqual(self.client.get(reverse("api:unidade", args=[999999])).status_code, 404)

    def test_catalogo_de_servicos(self):
        siglas = [s["sigla"] for s in self.client.get(reverse("api:servicos")).json()["resultados"]]
        self.assertIn("CRAS", siglas)
        self.assertNotIn("CTA", siglas)

    def test_metodo_nao_permitido(self):
        self.assertEqual(self.client.post(reverse("api:unidades")).status_code, 405)

    def test_pagina_de_servicos_paginada_e_com_script(self):
        resposta = self.client.get(reverse("servicos:lista"), {"tipo": "CRAS"})
        self.assertContains(resposta, "54 unidades encontradas")
        self.assertContains(resposta, "js/servicos.js")
