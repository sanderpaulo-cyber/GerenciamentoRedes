from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from gerenciamento_redes.models import NetworkDevice
from gerenciamento_redes.services.network_service import NetworkManagerService


class FakeDeviceRepository:
    def __init__(self) -> None:
        self._devices: list[NetworkDevice] = []
        self._last_id = 0

    def create(self, device: NetworkDevice) -> NetworkDevice:
        self._last_id += 1
        created = NetworkDevice(
            id=self._last_id,
            name=device.name,
            ip_address=device.ip_address,
            device_type=device.device_type,
            status=device.status,
            created_at=datetime.now(),
        )
        self._devices.append(created)
        return created

    def list_all(self) -> list[NetworkDevice]:
        return list(self._devices)

    def update_status(self, device_id: int, status: str) -> bool:
        for device in self._devices:
            if device.id == device_id:
                device.status = status
                return True
        return False


class NetworkManagerServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = FakeDeviceRepository()
        self.service = NetworkManagerService(self.repository)

    def test_cadastrar_dispositivo_com_sucesso(self) -> None:
        created = self.service.cadastrar_dispositivo(
            nome="Switch-01",
            ip_address="10.0.0.10",
            device_type="switch",
        )
        self.assertIsNotNone(created.id)
        self.assertEqual(created.status, "ativo")

    def test_cadastrar_dispositivo_falha_com_ip_invalido(self) -> None:
        with self.assertRaises(ValueError):
            self.service.cadastrar_dispositivo(
                nome="Firewall",
                ip_address="500.1.1.1",
                device_type="firewall",
            )

    def test_atualizar_status_com_sucesso(self) -> None:
        created = self.service.cadastrar_dispositivo(
            nome="Router-01",
            ip_address="192.168.1.1",
            device_type="router",
        )
        updated = self.service.atualizar_status(created.id or 0, "manutencao")
        self.assertTrue(updated)
        self.assertEqual(self.service.listar_dispositivos()[0].status, "manutencao")

    def test_atualizar_status_invalido(self) -> None:
        created = self.service.cadastrar_dispositivo(
            nome="AP-01",
            ip_address="10.10.10.10",
            device_type="access-point",
        )
        with self.assertRaises(ValueError):
            self.service.atualizar_status(created.id or 0, "quebrado")  # type: ignore[arg-type]

    def test_atualizar_status_retorna_false_se_id_nao_existe(self) -> None:
        updated = self.service.atualizar_status(999, "ativo")
        self.assertFalse(updated)


if __name__ == "__main__":
    unittest.main()
