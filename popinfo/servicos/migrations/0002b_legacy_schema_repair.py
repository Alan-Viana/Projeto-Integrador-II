from django.db import migrations


def reparar_esquema_legado(apps, schema_editor):
    connection = schema_editor.connection
    columns = {
        column.name
        for column in connection.introspection.get_table_description(
            connection.cursor(),
            "servicos_servico",
        )
    }

    missing_columns = {
        "nivel_protecao": "VARCHAR(10) NOT NULL DEFAULT 'NA'",
        "publico_alvo": "VARCHAR(255) NOT NULL DEFAULT ''",
        "como_acessar": "TEXT NOT NULL DEFAULT ''",
        "documentos_necessarios": "VARCHAR(255) NOT NULL DEFAULT ''",
    }
    for name, definition in missing_columns.items():
        if name not in columns:
            schema_editor.execute(
                f"ALTER TABLE servicos_servico ADD COLUMN {name} {definition}"
            )

    existing_tables = set(connection.introspection.table_names())
    for model_name in ("Acao", "Unidade"):
        model = apps.get_model("servicos", model_name)
        if model._meta.db_table not in existing_tables:
            schema_editor.create_model(model)


class Migration(migrations.Migration):

    dependencies = [
        ("servicos", "0002_servico_sigla"),
    ]

    operations = [
        migrations.RunPython(reparar_esquema_legado, migrations.RunPython.noop),
    ]
