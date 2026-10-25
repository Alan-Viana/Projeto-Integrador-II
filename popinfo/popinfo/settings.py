"""
Configurações do projeto PopInfo.

Projeto Integrador (PI) - UNIVESP
Plataforma de divulgação unificada de serviços socioassistenciais
na cidade de São Paulo.
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos base
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Segurança
#
# ATENÇÃO: as configurações abaixo são adequadas apenas para ambiente de
# desenvolvimento local (localhost). Antes de enviar o projeto para um
# ambiente de produção/nuvem, mova SECRET_KEY e DEBUG para variáveis de
# ambiente e restrinja ALLOWED_HOSTS.
# ---------------------------------------------------------------------------
SECRET_KEY = "django-insecure-popinfo-dev-key-troque-em-producao-000111222"

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


# ---------------------------------------------------------------------------
# Definição das aplicações
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Aplicações do PopInfo
    "core.apps.CoreConfig",
    "servicos.apps.ServicosConfig",
    "accounts.apps.AccountsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "popinfo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "popinfo.wsgi.application"


# ---------------------------------------------------------------------------
# Banco de dados
#
# SQLite é utilizado no ambiente de desenvolvimento local por não exigir
# configuração adicional. A camada de Repository foi construída de modo a
# isolar o acesso a dados, facilitando uma futura migração para PostgreSQL
# no ambiente de nuvem sem impactar as camadas de Service e Controller.
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ---------------------------------------------------------------------------
# Validação de senha
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------------------
# Internacionalização
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Arquivos estáticos (CSS, JavaScript, imagens)
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------------------
# Autenticação (Área Restrita)
# ---------------------------------------------------------------------------
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
