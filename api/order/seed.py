import random
from typing import List

from rapihogar.models import Order, Scheme, Technician, User


class OrderSeeder:

    @staticmethod
    def create_random_orders(
        technicians: List[Technician],
        clients: List[User],
        schemes: List[Scheme],
        n: int,
        max_hours: int = 10,
    ) -> List[Order]:
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
                Order(
                    technician=technician,
                    client=client,
                    scheme=scheme,
                    hours_worked=hours_worked,
                    type_request=Order.ORDER,
                )
            )

        return Order.objects.bulk_create(orders)

    @staticmethod
    def delete_all_orders() -> None:
        """
        Elimina todos los pedidos de la base de datos.
        """
        Order.objects.all().delete()
