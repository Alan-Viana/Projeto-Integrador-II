from django.db import migrations


def remover_coluna_legada(apps, schema_editor):
    connection = schema_editor.connection
    columns = {
        column.name
        for column in connection.introspection.get_table_description(
            connection.cursor(),
            "servicos_servico",
        )
    }
    if "tipo_sigla" not in columns:
        return

    schema_editor.execute(
        """
        CREATE TABLE servicos_servico_new (
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            sigla varchar(30) NOT NULL UNIQUE,
            nome varchar(150) NOT NULL,
            descricao text NOT NULL,
            nivel_protecao varchar(10) NOT NULL,
            publico_alvo varchar(255) NOT NULL,
            como_acessar text NOT NULL,
            documentos_necessarios varchar(255) NOT NULL,
            ativo bool NOT NULL,
            criado_em datetime NOT NULL,
            atualizado_em datetime NOT NULL,
            categoria_id bigint NOT NULL REFERENCES servicos_categoria (id)
        )
        """
    )
    schema_editor.execute(
        """
        INSERT INTO servicos_servico_new (
            id, sigla, nome, descricao, nivel_protecao, publico_alvo,
            como_acessar, documentos_necessarios, ativo, criado_em,
            atualizado_em, categoria_id
        )
        SELECT id, sigla, nome, descricao, nivel_protecao, publico_alvo,
               como_acessar, documentos_necessarios, ativo, criado_em,
               atualizado_em, categoria_id
        FROM servicos_servico
        """
    )
    schema_editor.execute("DROP TABLE servicos_servico")
    schema_editor.execute(
        "ALTER TABLE servicos_servico_new RENAME TO servicos_servico"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("servicos", "0002b_legacy_schema_repair"),
    ]

    operations = [
        migrations.RunPython(remover_coluna_legada, migrations.RunPython.noop),
    ]
