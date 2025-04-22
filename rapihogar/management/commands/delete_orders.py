from typing import Any

from django.core.management.base import BaseCommand, CommandError

from rapihogar.models import Order


class Command(BaseCommand):
    help: str = "Elimina todos los pedidos de la base de datos"
    """
    Este comando elimina todos los pedidos de la base de datos.
    Para ejecutar este comando, usa el siguiente comando en la terminal:
    python manage.py delete_orders --confirm
    """

    def handle(self, *args: Any, **kwargs: dict[str, Any]) -> None:

        confirmation: str = (
            input("¿Estás seguro de que deseas eliminar todos los pedidos? (s/N): ")
            .strip()
            .lower()
        )

        if confirmation != "s":
            self.stdout.write(self.style.WARNING("Eliminación cancelada."))
            return

        total_deleted, _ = Order.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(f"Se eliminaron {total_deleted} pedidos correctamente.")
        )
