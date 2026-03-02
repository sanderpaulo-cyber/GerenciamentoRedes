from __future__ import annotations

import argparse
from typing import Sequence

from gerenciamento_redes.db import create_mysql_connection
from gerenciamento_redes.repositories import MySQLDeviceRepository
from gerenciamento_redes.services import NetworkManagerService


STATUS_CHOICES = ("ativo", "manutencao", "inativo")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gerencia-redes",
        description="CLI para gerenciamento de dispositivos de rede.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    cadastrar_parser = subcommands.add_parser(
        "cadastrar", help="Cadastra um novo dispositivo."
    )
    cadastrar_parser.add_argument("--nome", required=True, help="Nome do dispositivo.")
    cadastrar_parser.add_argument("--ip", required=True, help="Endereco IP do dispositivo.")
    cadastrar_parser.add_argument(
        "--tipo", required=True, help="Tipo do dispositivo (router, switch, firewall...)."
    )
    cadastrar_parser.add_argument(
        "--status",
        choices=STATUS_CHOICES,
        default="ativo",
        help="Status inicial do dispositivo.",
    )

    subcommands.add_parser("listar", help="Lista dispositivos cadastrados.")

    status_parser = subcommands.add_parser(
        "status", help="Atualiza o status de um dispositivo."
    )
    status_parser.add_argument("--id", type=int, required=True, help="ID do dispositivo.")
    status_parser.add_argument("--status", choices=STATUS_CHOICES, required=True)

    return parser


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    connection = None
    try:
        connection = create_mysql_connection()
        repository = MySQLDeviceRepository(connection)
        service = NetworkManagerService(repository)

        if args.command == "cadastrar":
            created = service.cadastrar_dispositivo(
                nome=args.nome,
                ip_address=args.ip,
                device_type=args.tipo,
                status=args.status,
            )
            print(f"Dispositivo cadastrado com sucesso. ID: {created.id}")
            return 0

        if args.command == "listar":
            _print_devices(service.listar_dispositivos())
            return 0

        if args.command == "status":
            updated = service.atualizar_status(args.id, args.status)
            if not updated:
                print("Nenhum dispositivo encontrado para o ID informado.")
                return 1
            print("Status atualizado com sucesso.")
            return 0

        parser.error("Comando nao suportado.")
        return 2
    except ValueError as exc:
        print(f"Erro de validacao: {exc}")
        return 2
    except Exception as exc:  # pragma: no cover - erro de infra
        print(f"Erro ao executar comando: {exc}")
        return 1
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def _print_devices(devices) -> None:
    if not devices:
        print("Nenhum dispositivo cadastrado.")
        return

    print(f"{'ID':<4} {'NOME':<24} {'IP':<16} {'TIPO':<16} {'STATUS':<12}")
    print("-" * 76)
    for device in devices:
        print(
            f"{device.id:<4} "
            f"{device.name:<24} "
            f"{device.ip_address:<16} "
            f"{device.device_type:<16} "
            f"{device.status:<12}"
        )
