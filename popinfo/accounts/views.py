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
            return redirect("accounts:painel_unidades")
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
                return redirect(request.GET.get("next") or "accounts:painel_unidades")
            messages.error(request, "Usuário/e-mail ou senha inválidos.")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    """Encerra a sessão do usuário autenticado."""

    def post(self, request):
        auth_logout(request)
        return redirect("core:home")


# ---------------------------------------------------------------------------
# Painel da Área Restrita (requer login)
# ---------------------------------------------------------------------------
from django.contrib.auth.mixins import LoginRequiredMixin  # noqa: E402
from django.contrib.messages.views import SuccessMessageMixin  # noqa: E402
from django.db.models import Q  # noqa: E402
from django.shortcuts import get_object_or_404  # noqa: E402
from django.urls import reverse_lazy  # noqa: E402
from django.views.generic import CreateView, DeleteView, ListView, UpdateView  # noqa: E402

from core.forms import ContatoForm  # noqa: E402
from core.models import Mensagem  # noqa: E402
from servicos.models import Unidade  # noqa: E402

from .forms import UnidadeForm, UsuarioForm  # noqa: E402
from .models import Usuario  # noqa: E402

LISTA_UNIDADES = reverse_lazy("accounts:painel_unidades")


class UnidadePainelListView(LoginRequiredMixin, ListView):
    template_name = "accounts/painel/unidades.html"
    paginate_by = 25

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        unidades = Unidade.objects.select_related("servico").order_by("servico__sigla", "nome")
        if q:
            unidades = unidades.filter(
                Q(nome__icontains=q) | Q(bairro__icontains=q) | Q(servico__sigla__icontains=q)
            )
        return unidades


class UnidadeFormMixin(LoginRequiredMixin, SuccessMessageMixin):
    model = Unidade
    form_class = UnidadeForm
    template_name = "accounts/painel/unidade_form.html"
    success_url = LISTA_UNIDADES


class UnidadeCreateView(UnidadeFormMixin, CreateView):
    success_message = "Unidade cadastrada com sucesso."


class UnidadeUpdateView(UnidadeFormMixin, UpdateView):
    success_message = "Unidade atualizada com sucesso."


class UnidadeDeleteView(LoginRequiredMixin, DeleteView):
    model = Unidade
    success_url = LISTA_UNIDADES
    http_method_names = ["post"]  # a confirmação é feita na própria lista

    def form_valid(self, form):
        messages.success(self.request, f"Unidade \"{self.object.nome}\" excluída.")
        return super().form_valid(form)


class UsuarioPainelView(LoginRequiredMixin, View):
    template_name = "accounts/painel/usuarios.html"

    def _render(self, request, form):
        usuarios = Usuario.objects.select_related("user")
        return render(request, self.template_name, {"form": form, "usuarios": usuarios})

    def get(self, request):
        return self._render(request, UsuarioForm())

    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f"Usuário \"{usuario.user.username}\" cadastrado.")
            return redirect("accounts:painel_usuarios")
        return self._render(request, form)


class MensagemPainelView(LoginRequiredMixin, ListView):
    template_name = "accounts/painel/mensagens.html"
    paginate_by = 20

    def get_queryset(self):
        mensagens = Mensagem.objects.all()
        assunto = self.request.GET.get("assunto")
        status = self.request.GET.get("status")
        if assunto:
            mensagens = mensagens.filter(assunto=assunto)
        if status in ("lidas", "nao_lidas"):
            mensagens = mensagens.filter(lida=(status == "lidas"))
        return mensagens

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["assuntos"] = ContatoForm.ASSUNTO_CHOICES[1:]
        ctx["nao_lidas"] = Mensagem.objects.filter(lida=False).count()
        return ctx

    def post(self, request):
        """Alterna o status lida/não lida de uma mensagem."""
        mensagem = get_object_or_404(Mensagem, pk=request.POST.get("id"))
        mensagem.lida = not mensagem.lida
        mensagem.save(update_fields=["lida"])
        return redirect(request.get_full_path())
