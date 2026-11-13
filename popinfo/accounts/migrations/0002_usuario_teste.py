"""Cria o usuário universal de teste da Área Restrita (userteste / 12345)."""
from django.contrib.auth.hashers import make_password
from django.db import migrations


def criar(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Usuario = apps.get_model("accounts", "Usuario")
    user, _ = User.objects.get_or_create(
        username="userteste",
        defaults={"password": make_password("12345"), "is_staff": True, "is_superuser": True},
    )
    Usuario.objects.get_or_create(user=user, defaults={"nome": "Usuário de Teste", "cargo": "Administrador"})


def remover(apps, schema_editor):
    apps.get_model("auth", "User").objects.filter(username="userteste").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(criar, remover),
    ]
