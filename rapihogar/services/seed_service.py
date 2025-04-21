import random
from typing import List

from rapihogar.models import Pedido, Scheme, Technician, User


class PedidoService:

    @staticmethod
    def create_random_pedidos(
        technicians: List[Technician],
        clients: List[User],
        schemes: List[Scheme],
        n: int,
        max_hours: int = 10,
    ) -> List[Pedido]:
        """
        Crea múltiples pedidos aleatorios seleccionando técnicos, clientes y esquemas al azar.
        Inserta los pedidos en la base de datos de forma masiva.
        """
        if not technicians or not clients or not schemes:
            raise ValueError(
                "Asegúrate de tener técnicos, clientes y esquemas en la base de datos."
            )

        MIN_HOURS: int = 1
        if max_hours < MIN_HOURS:
            raise ValueError("max_hours debe ser al menos 1.")

        orders = []
        for _ in range(n):
            technician = random.choice(technicians)
            client = random.choice(clients)
            scheme = random.choice(schemes)
            hours_worked = random.randint(MIN_HOURS, max_hours)

            orders.append(
                Pedido(
                    technician=technician,
                    client=client,
                    scheme=scheme,
                    hours_worked=hours_worked,
                    type_request=Pedido.PEDIDO,
                )
            )

        return Pedido.objects.bulk_create(orders)

    @staticmethod
    def delete_all_orders() -> None:
        """
        Elimina todos los pedidos de la base de datos.
        """
        Pedido.objects.all().delete()
