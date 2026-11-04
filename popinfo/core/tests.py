from django.test import TestCase
from django.urls import reverse

class CorePagesTestCase(TestCase):
    """
    Classe de testes unitários para verificar a acessibilidade
    das páginas estáticas e institucionais do aplicativo core.
    """

    def test_home_status_code(self):
        """Garante que a página inicial (home) carrega com sucesso (HTTP 200)."""
        response = self.client.get(reverse('core:home'))  # Assume que a rota home tem o namespace core:home
        self.assertEqual(response.status_code, 200)

    def test_sobre_status_code(self):
        """Garante que a página 'Sobre' carrega com sucesso (HTTP 200)."""
        response = self.client.get(reverse('core:sobre'))
        self.assertEqual(response.status_code, 200)