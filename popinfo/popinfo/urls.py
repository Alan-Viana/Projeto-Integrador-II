"""
Roteamento raiz do projeto PopInfo.

Cada aplicação (core, servicos, accounts) mantém seu próprio arquivo de
rotas, mantendo o projeto organizado por domínio/funcionalidade.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("servicos/", include("servicos.urls")),
    path("conta/", include("accounts.urls")),
    path("api/", include("servicos.api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
