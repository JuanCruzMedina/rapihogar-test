from typing import Any, Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rapihogar.models import Order, Scheme, Technician, User


class TechnicianReportViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Configura los datos iniciales para las pruebas (se ejecuta una sola vez).
        """

        cls.technician1 = Technician.objects.create(
            first_name="Juan", last_name="Perez"
        )
        cls.technician2 = Technician.objects.create(
            first_name="Maria", last_name="Lopez"
        )
        cls.technician3 = Technician.objects.create(
            first_name="Carlos", last_name="Juan"
        )

        cls.client = User.objects.create(
            first_name="Cliente",
            last_name="Prueba",
            email="cliente@prueba.com",
            username="clienteprueba",
        )
        cls.scheme = Scheme.objects.create(name="Esquema de prueba")

        Order.objects.create(
            technician=cls.technician1,
            client=cls.client,
            scheme=cls.scheme,
            hours_worked=10,
            type_request=Order.ORDER,
        )
        Order.objects.create(
            technician=cls.technician1,
            client=cls.client,
            scheme=cls.scheme,
            hours_worked=5,
            type_request=Order.ORDER,
        )
        Order.objects.create(
            technician=cls.technician3,
            client=cls.client,
            scheme=cls.scheme,
            hours_worked=8,
            type_request=Order.ORDER,
        )

    def test_report_structure(self) -> None:
        """
        Verifica que la estructura del informe sea consistente.
        """
        response = self.client.get(reverse("technician-report"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data: Dict[str, Any] = response.json()
        self.assertIn("average_payment", data)
        self.assertIn("below_average_technicians", data)
        self.assertIn("lowest_paid_technician", data)
        self.assertIn("highest_paid_technician", data)

    def test_average_payment(self) -> None:
        """
        Verifica que el monto promedio cobrado por los técnicos sea correcto.
        """
        response = self.client.get(reverse("technician-report"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data: Dict[str, Any] = response.json()
        self.assertAlmostEqual(data["average_payment"], 1503.33, places=2)

    def test_below_average_technicians(self) -> None:
        """
        Verifica que los técnicos por debajo del promedio sean correctos.
        """
        response = self.client.get(reverse("technician-report"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data: Dict[str, Any] = response.json()
        below_average = data["below_average_technicians"]
        self.assertEqual(len(below_average), 2)
        self.assertEqual(below_average[0]["full_name"], "Maria Lopez")
        self.assertEqual(below_average[1]["full_name"], "Carlos Juan")

    def test_lowest_paid_technician(self) -> None:
        """
        Verifica que el técnico con el monto más bajo sea correcto.
        """
        response = self.client.get(reverse("technician-report"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data: Dict[str, Any] = response.json()
        lowest_paid = data["lowest_paid_technician"]
        self.assertIsNotNone(lowest_paid)
        self.assertEqual(lowest_paid["full_name"], "Maria Lopez")
        self.assertEqual(lowest_paid["total_payment"], 0)

    def test_highest_paid_technician(self) -> None:
        """
        Verifica que el técnico con el monto más alto sea correcto.
        """
        response = self.client.get(reverse("technician-report"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data: Dict[str, Any] = response.json()
        highest_paid = data["highest_paid_technician"]
        self.assertIsNotNone(highest_paid)
        self.assertEqual(highest_paid["full_name"], "Juan Perez")
        self.assertEqual(highest_paid["total_payment"], 3150)
