from typing import Any, Dict, List

from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rapihogar.models import Pedido, Scheme, Technician, User

FULL_NAME_JUAN = "Juan Perez"
FULL_NAME_MARIA = "Maria Lopez"
FULL_NAME_CARLOS = "Carlos Juan"


class TechnicianPaymentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Configura los datos iniciales para las pruebas (se ejecuta una sola vez).
        """
        Technician.objects.create(first_name="Juan", last_name="Perez")
        Technician.objects.create(first_name="Maria", last_name="Lopez")
        Technician.objects.create(first_name="Carlos", last_name="Juan")

    def test_filter_by_name(self) -> None:
        """
        Verifica que el filtro por nombre funcione correctamente.
        """
        test_cases = [
            {
                "name_filter": "Juan",
                "expected_count": 2,
                "expected_names": ["Juan Perez", "Carlos Juan"],
            },
            {
                "name_filter": "Maria",
                "expected_count": 1,
                "expected_names": ["Maria Lopez"],
            },
            {
                "name_filter": "Mar",
                "expected_count": 1,
                "expected_names": ["Maria Lopez"],
            },
            {"name_filter": "Nonexistent", "expected_count": 0, "expected_names": []},
        ]

        for case in test_cases:
            with self.subTest(name_filter=case["name_filter"]):
                response: JsonResponse = self.client.get(
                    reverse("technician-payments-list"), {"name": case["name_filter"]}
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                response_data: List[Dict[str, Any]] = response.json()
                self.assertEqual(len(response_data), case["expected_count"])
                self.assertEqual(
                    [technician["full_name"] for technician in response_data],
                    case["expected_names"],
                )

    def test_no_filter_returns_all_technicians(self) -> None:
        """
        Verifica que sin filtro se devuelvan todos los técnicos.
        """
        response: JsonResponse = self.client.get(reverse("technician-payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: List[Dict[str, Any]] = response.json()
        self.assertEqual(len(response_data), 3)
        response_technicians: List[str] = [
            technician["full_name"] for technician in response_data
        ]
        self.assertIn(FULL_NAME_JUAN, response_technicians)
        self.assertIn(FULL_NAME_MARIA, response_technicians)
        self.assertIn(FULL_NAME_CARLOS, response_technicians)

    def test_no_technicians(self) -> None:
        """
        Verifica que el endpoint funcione correctamente cuando no hay técnicos.
        """
        Technician.objects.all().delete()
        response: JsonResponse = self.client.get(reverse("technician-payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: List[Dict[str, Any]] = response.json()
        self.assertEqual(len(response_data), 0)

    def test_response_structure(self) -> None:
        """
        Verifica que la estructura de la respuesta sea consistente.
        """
        response: JsonResponse = self.client.get(reverse("technician-payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: List[Dict[str, Any]] = response.json()

        for technician in response_data:
            self.assertIn("full_name", technician)
            self.assertIn("total_hours", technician)
            self.assertIn("total_payment", technician)
            self.assertIn("total_orders", technician)

    def test_calculated_fields_with_orders(self) -> None:
        """
        Verifica que los campos calculados (total_hours, total_payment, total_orders)
        sean correctos para técnicos con pedidos.
        """
        technician = Technician.objects.get(first_name="Juan", last_name="Perez")
        user = User.objects.create(
            first_name="Cliente",
            last_name="Uno",
            email="cliente@uno.com",
            username="clienteuno",
        )
        scheme = Scheme.objects.create(
            name="Esquema de prueba",
        )
        technician.pedido_set.create(
            type_request=Pedido.PEDIDO, client=user, scheme=scheme, hours_worked=5
        )
        technician.pedido_set.create(
            type_request=Pedido.PEDIDO, client=user, scheme=scheme, hours_worked=3
        )

        response: JsonResponse = self.client.get(reverse("technician-payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: List[Dict[str, Any]] = response.json()

        juan_data = next(
            (
                technician
                for technician in response_data
                if technician["full_name"] == FULL_NAME_JUAN
            ),
            None,
        )
        self.assertIsNotNone(juan_data)
        self.assertEqual(juan_data["total_hours"], 8)
        self.assertEqual(juan_data["total_payment"], 1360)
        self.assertEqual(juan_data["total_orders"], 2)

    def test_calculated_fields_no_orders(self) -> None:
        """
        Verifica que los campos calculados sean correctos para técnicos sin pedidos.
        """
        response: JsonResponse = self.client.get(reverse("technician-payments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: List[Dict[str, Any]] = response.json()

        maria_data = next(
            (
                technician
                for technician in response_data
                if technician["full_name"] == FULL_NAME_MARIA
            ),
            None,
        )
        self.assertIsNotNone(maria_data)
        self.assertEqual(maria_data["total_hours"], 0)
        self.assertEqual(maria_data["total_payment"], 0)
        self.assertEqual(maria_data["total_orders"], 0)
