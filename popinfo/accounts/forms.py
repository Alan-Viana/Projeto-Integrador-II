"""Formulários da aplicação de autenticação."""
from django import forms


class LoginForm(forms.Form):
    """Formulário de acesso à Área Restrita.

    Observação: nesta etapa (foco em frontend) o formulário apenas
    valida os campos e envia a tentativa de autenticação para a camada
    de Service. A criação de usuários administrativos deve ser feita
    via `python manage.py createsuperuser`, utilizando o e-mail como
    nome de usuário.
    """

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "seu@email.com",
                "autofocus": True,
            }
        ),
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "••••••••",
            }
        ),
    )
