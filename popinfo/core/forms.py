"""Formulários da aplicação principal."""
from django import forms


class ContatoForm(forms.Form):
    """Formulário exibido na página Contato."""

    ASSUNTO_CHOICES = [
        ("", "Selecione um assunto"),
        ("duvida", "Dúvida sobre um serviço"),
        ("sugestao", "Sugestão de melhoria"),
        ("cadastro", "Cadastro de nova instituição/ONG"),
        ("erro", "Reportar informação incorreta"),
        ("outro", "Outro assunto"),
    ]

    nome_completo = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nome completo",
            }
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "seu@email.com",
            }
        ),
    )
    telefone = forms.CharField(
        label="Telefone",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "(11) 0000-0000",
            }
        ),
    )
    assunto = forms.ChoiceField(
        label="Assunto",
        choices=ASSUNTO_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    mensagem = forms.CharField(
        label="Mensagem",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Descreva detalhadamente sua dúvida, sugestão ou solicitação...",
            }
        ),
    )
