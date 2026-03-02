from __future__ import annotations

import ipaddress

from gerenciamento_redes.models import DeviceStatus, NetworkDevice
from gerenciamento_redes.repositories.device_repository import DeviceRepository


class NetworkManagerService:
    VALID_STATUSES = {"ativo", "manutencao", "inativo"}

    def __init__(self, repository: DeviceRepository) -> None:
        self._repository = repository

    def cadastrar_dispositivo(
        self,
        nome: str,
        ip_address: str,
        device_type: str,
        status: DeviceStatus = "ativo",
    ) -> NetworkDevice:
        if not nome.strip():
            raise ValueError("Nome do dispositivo nao pode ser vazio.")
        if not device_type.strip():
            raise ValueError("Tipo do dispositivo nao pode ser vazio.")
        self._validate_ip(ip_address)
        self._validate_status(status)

        device = NetworkDevice(
            id=None,
            name=nome.strip(),
            ip_address=ip_address.strip(),
            device_type=device_type.strip(),
            status=status,
        )
        return self._repository.create(device)

    def listar_dispositivos(self) -> list[NetworkDevice]:
        return self._repository.list_all()

    def atualizar_status(self, device_id: int, status: DeviceStatus) -> bool:
        if device_id <= 0:
            raise ValueError("ID do dispositivo deve ser maior que zero.")
        self._validate_status(status)
        return self._repository.update_status(device_id, status)

    @staticmethod
    def _validate_ip(ip_address: str) -> None:
        try:
            ipaddress.ip_address(ip_address.strip())
        except ValueError as exc:
            raise ValueError("Endereco IP invalido.") from exc

    @classmethod
    def _validate_status(cls, status: str) -> None:
        if status not in cls.VALID_STATUSES:
            raise ValueError(
                f"Status invalido: {status}. "
                f"Use um dos valores: {', '.join(sorted(cls.VALID_STATUSES))}."
            )
