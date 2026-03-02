from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from gerenciamento_redes.models import DeviceStatus, NetworkDevice

if TYPE_CHECKING:
    from mysql.connector.abstracts import MySQLConnectionAbstract


class DeviceRepository(Protocol):
    def create(self, device: NetworkDevice) -> NetworkDevice:
        raise NotImplementedError

    def list_all(self) -> list[NetworkDevice]:
        raise NotImplementedError

    def update_status(self, device_id: int, status: DeviceStatus) -> bool:
        raise NotImplementedError


class MySQLDeviceRepository:
    def __init__(self, connection: "MySQLConnectionAbstract") -> None:
        self._connection = connection

    def create(self, device: NetworkDevice) -> NetworkDevice:
        query = """
            INSERT INTO devices (name, ip_address, device_type, status)
            VALUES (%s, %s, %s, %s)
        """
        params = (device.name, device.ip_address, device.device_type, device.status)

        cursor = self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        device_id = cursor.lastrowid
        cursor.close()

        created = self._get_by_id(device_id)
        if created is None:
            raise RuntimeError("Falha ao recuperar dispositivo apos insercao.")
        return created

    def list_all(self) -> list[NetworkDevice]:
        query = """
            SELECT id, name, ip_address, device_type, status, created_at
            FROM devices
            ORDER BY id ASC
        """
        cursor = self._connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return [self._map_row(row) for row in rows]

    def update_status(self, device_id: int, status: DeviceStatus) -> bool:
        query = "UPDATE devices SET status = %s WHERE id = %s"
        cursor = self._connection.cursor()
        cursor.execute(query, (status, device_id))
        self._connection.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        return updated

    def _get_by_id(self, device_id: int) -> NetworkDevice | None:
        query = """
            SELECT id, name, ip_address, device_type, status, created_at
            FROM devices
            WHERE id = %s
        """
        cursor = self._connection.cursor(dictionary=True)
        cursor.execute(query, (device_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        return self._map_row(row)

    @staticmethod
    def _map_row(row: dict[str, object]) -> NetworkDevice:
        return NetworkDevice(
            id=int(row["id"]),
            name=str(row["name"]),
            ip_address=str(row["ip_address"]),
            device_type=str(row["device_type"]),
            status=str(row["status"]),  # type: ignore[arg-type]
            created_at=row.get("created_at"),  # type: ignore[arg-type]
        )
