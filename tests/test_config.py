from __future__ import annotations

import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from gerenciamento_redes.config import DatabaseSettings


class DatabaseSettingsTestCase(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "DB_HOST": "db-interno",
            "DB_PORT": "3307",
            "DB_USER": "admin",
            "DB_PASSWORD": "segredo",
            "DB_NAME": "redes",
            "DB_AUTOCOMMIT": "false",
        },
        clear=True,
    )
    def test_from_env_lendo_variaveis(self) -> None:
        settings = DatabaseSettings.from_env()
        self.assertEqual(settings.host, "db-interno")
        self.assertEqual(settings.port, 3307)
        self.assertEqual(settings.user, "admin")
        self.assertEqual(settings.password, "segredo")
        self.assertEqual(settings.name, "redes")
        self.assertFalse(settings.autocommit)

    @patch.dict(os.environ, {}, clear=True)
    def test_from_env_com_defaults(self) -> None:
        settings = DatabaseSettings.from_env()
        self.assertEqual(settings.host, "localhost")
        self.assertEqual(settings.port, 3306)
        self.assertEqual(settings.user, "redes_user")
        self.assertEqual(settings.password, "redes_pass")
        self.assertEqual(settings.name, "gerenciamento_redes")
        self.assertTrue(settings.autocommit)

    @patch.dict(os.environ, {"DB_PORT": "3308"}, clear=True)
    def test_dsn(self) -> None:
        settings = DatabaseSettings.from_env()
        self.assertEqual(
            settings.dsn(),
            "mysql://redes_user:redes_pass@localhost:3308/gerenciamento_redes",
        )


if __name__ == "__main__":
    unittest.main()
