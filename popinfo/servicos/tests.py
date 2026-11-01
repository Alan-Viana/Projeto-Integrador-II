from django.test import TestCase
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