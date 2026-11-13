"""Formulários da Área Restrita."""
from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from servicos.models import Unidade

from .models import Usuario

User = get_user_model()


class LoginForm(forms.Form):
    """Acesso à Área Restrita por nome de usuário ou e-mail."""

    email = forms.CharField(
        label="Usuário ou e-mail",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "usuário ou seu@email.com",
                                      "autofocus": True, "autocomplete": "username"}),
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "••••••••",
                                          "autocomplete": "current-password"}),
    )


class BootstrapMixin:
    """Aplica as classes do Bootstrap a todos os campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            w = campo.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs["class"] = "form-check-input"
            elif isinstance(w, forms.Select):
                w.attrs["class"] = "form-select"
            else:
                w.attrs["class"] = "form-control"
            if isinstance(w, forms.Textarea):
                w.attrs["rows"] = 3


class UnidadeForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Unidade
        exclude = ["criado_em", "atualizado_em"]
        widgets = {"verificado_em": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}


class UsuarioForm(BootstrapMixin, forms.Form):
    """Cadastro de funcionário da ONG (cria o login e o perfil)."""

    nome = forms.CharField(max_length=150)
    username = forms.CharField(label="Nome de usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    cargo = forms.CharField(max_length=100, required=False)
    telefone = forms.CharField(max_length=20, required=False)
    senha = forms.CharField(widget=forms.PasswordInput, min_length=5)
    confirmar_senha = forms.CharField(label="Confirmar senha", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nome de usuário já existe.")
        return username

    def clean(self):
        dados = super().clean()
        if dados.get("senha") != dados.get("confirmar_senha"):
            self.add_error("confirmar_senha", "As senhas não conferem.")
        return dados

    @transaction.atomic
    def save(self) -> Usuario:
        d = self.cleaned_data
        user = User.objects.create_user(username=d["username"], email=d["email"], password=d["senha"])
        return Usuario.objects.create(user=user, nome=d["nome"], cargo=d["cargo"], telefone=d["telefone"])
