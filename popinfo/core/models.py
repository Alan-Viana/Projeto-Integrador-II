"""Entidades da aplicação principal."""
from django.db import models

from .forms import ContatoForm


class Mensagem(models.Model):
    """Mensagem enviada pelo formulário da página Contato."""

    nome_completo = models.CharField(max_length=150)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    assunto = models.CharField(max_length=20, choices=ContatoForm.ASSUNTO_CHOICES[1:])
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    recebida_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ["lida", "-recebida_em"]

    def __str__(self) -> str:
        return f"{self.get_assunto_display()} — {self.nome_completo}"
