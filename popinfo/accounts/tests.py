from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Mensagem
from servicos.models import Servico, Unidade

from .models import Usuario


class AreaRestritaTestCase(TestCase):

    def entrar(self):
        return self.client.post(reverse("accounts:login"), {"email": "userteste", "senha": "12345"})

    def test_usuario_universal_faz_login(self):
        self.assertRedirects(self.entrar(), reverse("accounts:painel_unidades"))

    def test_painel_exige_login(self):
        resposta = self.client.get(reverse("accounts:painel_unidades"))
        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse("accounts:login"), resposta.url)

    def test_crud_de_unidade(self):
        self.entrar()
        servico = Servico.objects.get(sigla="CRAS")
        dados = {"servico": servico.pk, "nome": "Unidade Nova", "endereco": "Rua A, 1",
                 "bairro": "Centro", "cidade": "São Paulo", "ativo": "on"}
        self.client.post(reverse("accounts:unidade_criar"), dados)
        unidade = Unidade.objects.get(nome="Unidade Nova")

        dados["nome"] = "Unidade Editada"
        self.client.post(reverse("accounts:unidade_editar", args=[unidade.pk]), dados)
        unidade.refresh_from_db()
        self.assertEqual(unidade.nome, "Unidade Editada")

        self.client.post(reverse("accounts:unidade_excluir", args=[unidade.pk]))
        self.assertFalse(Unidade.objects.filter(pk=unidade.pk).exists())

    def test_cadastro_de_usuario_e_login_por_email(self):
        self.entrar()
        self.client.post(reverse("accounts:painel_usuarios"), {
            "nome": "Maria", "username": "maria", "email": "maria@ong.org",
            "senha": "segredo1", "confirmar_senha": "segredo1",
        })
        self.assertTrue(Usuario.objects.filter(user__username="maria").exists())
        self.client.post(reverse("accounts:logout"))
        resposta = self.client.post(reverse("accounts:login"), {"email": "maria@ong.org", "senha": "segredo1"})
        self.assertRedirects(resposta, reverse("accounts:painel_unidades"))

    def test_mensagem_de_contato_chega_no_painel(self):
        self.client.post(reverse("core:contato"), {
            "nome_completo": "João", "email": "joao@x.com", "assunto": "duvida", "mensagem": "Olá!",
        })
        mensagem = Mensagem.objects.get()
        self.entrar()
        self.assertContains(self.client.get(reverse("accounts:painel_mensagens")), "João")
        self.client.post(reverse("accounts:painel_mensagens"), {"id": mensagem.pk})
        mensagem.refresh_from_db()
        self.assertTrue(mensagem.lida)
        self.assertEqual(get_user_model().objects.filter(username="userteste").count(), 1)

    def test_telas_do_painel_renderizam(self):
        self.entrar()
        unidade = Unidade.objects.first()
        for url in [reverse("accounts:painel_unidades") + "?q=CRAS", reverse("accounts:unidade_criar"),
                    reverse("accounts:unidade_editar", args=[unidade.pk]), reverse("accounts:painel_usuarios"),
                    reverse("accounts:painel_mensagens")]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
