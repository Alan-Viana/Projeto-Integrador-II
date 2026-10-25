"""Camada de Controller (Views) da aplicação de autenticação."""
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.views import View

from .forms import LoginForm
from .services import AutenticacaoService


class LoginView(View):
    """Página de acesso à Área Restrita."""

    template_name = "accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:home")
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = AutenticacaoService().autenticar(
                email=form.cleaned_data["email"],
                senha=form.cleaned_data["senha"],
            )
            if usuario is not None:
                auth_login(request, usuario)
                return redirect("core:home")
            messages.error(request, "E-mail ou senha inválidos.")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    """Encerra a sessão do usuário autenticado."""

    def post(self, request):
        auth_logout(request)
        return redirect("core:home")
