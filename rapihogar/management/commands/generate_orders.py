from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from rapihogar.models import Scheme, Technician, User
from rapihogar.services.seed_service import PedidoService


class Command(BaseCommand):
    help: str = """
    Este comando genera un número específico de pedidos aleatorios en la base de datos.
    Para ejecutar este comando,
    usa el siguiente comando en la terminal:
    python manage.py generate_orders <n> [--delete]
    Donde <n> es el número de pedidos a generar (entre 1 y 100).
    El argumento --delete elimina todos los pedidos previos que estaban en la base de datos.
    """

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "n",
            type=int,
            help="Número de pedidos a generar (entre 1 y 100)",
        )
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Elimina todos los pedidos previos que estaban en la base de datos",
        )

    def handle(self, *args: Any, **kwargs: dict[str, Any]) -> None:

        if not settings.DEBUG:
            raise CommandError("Este comando solo se puede ejecutar en modo DEBUG.")

        n: int = kwargs["n"]
        delete: bool = kwargs["delete"]

        if delete:
            PedidoService.delete_all_orders()
            self.stdout.write(
                self.style.SUCCESS(
                    "Se eliminaron todos los pedidos previos correctamente."
                )
            )

        MIN_ORDERS: int = 1
        MAX_ORDERS: int = 100
        if not (MIN_ORDERS <= n <= MAX_ORDERS):
            raise CommandError(
                f"El número de pedidos debe estar entre {MIN_ORDERS} y {MAX_ORDERS}."
            )

        technicians = list(Technician.objects.all())
        clients = list(User.objects.filter(is_staff=False))
        schemes = list(Scheme.objects.all())

        if not technicians:
            raise CommandError("No hay técnicos disponibles en la base de datos.")
        if not clients:
            raise CommandError("No hay clientes disponibles en la base de datos.")
        if not schemes:
            raise CommandError("No hay esquemas disponibles en la base de datos.")

        PedidoService.create_random_pedidos(technicians, clients, schemes, n)

        self.stdout.write(
            self.style.SUCCESS(f"Se generaron {n} pedidos correctamente.")
        )
