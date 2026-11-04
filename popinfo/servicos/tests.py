from django.test import TestCase
from django.urls import reverse
from servicos.models import Servico, Categoria

class ServicoModelTestCase(TestCase):
    """
    Classe de testes unitários para validar a criação e persistência
    dos dados de unidades socioassistenciais no banco de dados.
    """

    def setUp(self):
        """Método executado antes de cada teste para configurar dados iniciais."""

        # 1. Cria uma categoria de teste para satisfazer a restrição (Foreign Key)
        self.categoria_teste = Categoria.objects.create(
            nome="Proteção Social Básica"
        )

        # 2. Inclui a categoria nos dados do serviço
        self.dados_servico = {
            'nome': 'CRAS Teste Sul',
            'descricao': 'Unidade de atendimento de teste para a Proteção Social Básica.',
            'endereco': 'Rua Exemplo, 123',
            'telefone': '(11) 99999-9999',
            'categoria': self.categoria_teste  # Associa a categoria obrigatória
        }

    def test_criacao_servico(self):
        """Testa se um novo serviço/unidade socioassistencial é criado com sucesso."""
        # Cria o registo no banco de dados de testes
        servico = Servico.objects.create(**self.dados_servico)

        # Verifica se o ID foi gerado (indicando salvamento)
        self.assertIsNotNone(servico.id)
        # Comprova se o nome salvo corresponde ao inserido
        self.assertEqual(servico.nome, 'CRAS Teste Sul')
        # Confirma se a categoria foi vinculada corretamente
        self.assertEqual(servico.categoria, self.categoria_teste)

class ServicoIntegrationTestCase(TestCase):
    """
    Classe de testes de integração para verificar o fluxo completo
    entre a View, o Modelo e o Template HTML de listagem de serviços.
    """

    def setUp(self):
        """Prepara o cenário com uma categoria e uma unidade socioassistencial."""
        self.categoria = Categoria.objects.create(
            nome="Proteção Social Básica"
        )
        self.servico = Servico.objects.create(
            nome="CRAS Vila Esperança",
            descricao="Unidade de atendimento regional.",
            endereco="Rua das Flores, 500",
            telefone="(11) 88888-8888",
            categoria=self.categoria
        )

    def test_fluxo_listagem_servicos_exibe_dados_no_html(self):
        """
        Testa se a página de listagem de serviços responde com sucesso (200 OK)
        e se exibe corretamente o nome e o endereço do serviço cadastrado na tela.
        """
        # Faz uma requisição GET para a rota de listagem de serviços
        response = self.client.get(reverse('servicos:lista'))

        # 1. Verifica se a página carregou com sucesso
        self.assertEqual(response.status_code, 200)

        # 2. Verifica se o nome do serviço inserido aparece no HTML renderizado
        self.assertContains(response, "CRAS Vila Esperança")

        # 3. Verifica se o endereço também está presente na página
        self.assertContains(response, "Rua das Flores, 500")