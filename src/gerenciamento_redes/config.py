from __future__ import annotations

from dataclasses import dataclass
import os


def _str_to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "t", "yes", "y"}


@dataclass(frozen=True)
class DatabaseSettings:
    host: str = "localhost"
    port: int = 3306
    user: str = "redes_user"
    password: str = "redes_pass"
    name: str = "gerenciamento_redes"
    autocommit: bool = True

    @classmethod
    def from_env(cls) -> "DatabaseSettings":
        return cls(
            host=os.getenv("DB_HOST", cls.host),
            port=int(os.getenv("DB_PORT", str(cls.port))),
            user=os.getenv("DB_USER", cls.user),
            password=os.getenv("DB_PASSWORD", cls.password),
            name=os.getenv("DB_NAME", cls.name),
            autocommit=_str_to_bool(os.getenv("DB_AUTOCOMMIT", str(cls.autocommit))),
        )

    def as_mysql_connector_kwargs(self) -> dict[str, object]:
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.name,
            "autocommit": self.autocommit,
        }

    def dsn(self) -> str:
        return (
            f"mysql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )
