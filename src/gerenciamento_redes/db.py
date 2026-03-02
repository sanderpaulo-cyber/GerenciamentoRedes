from __future__ import annotations

from gerenciamento_redes.config import DatabaseSettings


def create_mysql_connection(settings: DatabaseSettings | None = None):
    resolved_settings = settings or DatabaseSettings.from_env()

    try:
        import mysql.connector
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Dependencia ausente: instale mysql-connector-python para conectar ao MySQL."
        ) from exc

    return mysql.connector.connect(**resolved_settings.as_mysql_connector_kwargs())
