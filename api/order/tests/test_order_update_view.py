from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rapihogar.models import Order, Scheme, Technician, User


class OrderUpdateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Configura los datos iniciales para las pruebas.
        """
        cls.client_user: User = User.objects.create(
            first_name="Cliente",
            last_name="Prueba",
            email="cliente@prueba.com",
            username="clienteprueba",
        )
        cls.scheme: Scheme = Scheme.objects.create(name="Esquema de prueba")
        cls.technician1: Technician = Technician.objects.create(
            first_name="Juan", last_name="Perez"
        )
        cls.technician2: Technician = Technician.objects.create(
            first_name="Maria", last_name="Lopez"
        )

        cls.valid_order: Order = Order.objects.create(
            technician=cls.technician1,
            client=cls.client_user,
            scheme=cls.scheme,
            hours_worked=5,
            type_request=Order.ORDER,
        )

        cls.non_editable_order: Order = Order.objects.create(
            technician=cls.technician2,
            client=cls.client_user,
            scheme=cls.scheme,
            hours_worked=10,
            type_request=2,
        )

    def test_update_order_success(self) -> None:
        """
        Verifica que se pueda actualizar un pedido cuando type_request = PEDIDO.
        """
        url: str = reverse("order-update", args=[self.valid_order.id])
        new_data: dict = {
            "hours_worked": 8,
            "technician": self.technician2.id,
            "client": self.client_user.id,
            "scheme": self.scheme.id,
        }
        response = self.client.patch(url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_order: Order = Order.objects.get(id=self.valid_order.id)
        self.assertEqual(updated_order.hours_worked, 8)
        self.assertEqual(updated_order.technician.id, self.technician2.id)

    def test_update_order_not_pedido(self) -> None:
        """
        Verifica que no se pueda actualizar un pedido si type_request != PEDIDO.
        """
        url: str = reverse("order-update", args=[self.non_editable_order.id])
        new_data: dict = {"hours_worked": 15}
        response = self.client.patch(url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Solo se pueden modificar pedidos",
            str(response.data),
        )

    def test_update_non_existent_order(self) -> None:
        """
        Verifica el comportamiento al intentar actualizar un pedido que no existe.
        """
        url: str = reverse("order-update", args=[999])
        response = self.client.patch(url, {"hours_worked": 10}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_invalid_data(self) -> None:
        """
        Verifica que no se puedan enviar datos inválidos para un pedido.
        """
        url: str = reverse("order-update", args=[self.valid_order.id])
        invalid_hours_worked: int = -5
        new_data: dict = {"hours_worked": invalid_hours_worked}
        response = self.client.patch(url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
