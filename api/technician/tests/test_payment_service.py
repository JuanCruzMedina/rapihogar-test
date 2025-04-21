import unittest
from typing import Dict, List

from api.technician.services.payment_service import PaymentService


class TestPaymentService(unittest.TestCase):
    def test_calculate_payment_first_range_limits(self) -> None:
        """
        Verifica el cálculo para los límites del primer rango (0-14 horas).
        """
        test_cases: List[Dict[str, int]] = [
            {"hours": 0, "expected_payment": 0},
            {"hours": 14, "expected_payment": 2380},
        ]
        for case in test_cases:
            with self.subTest(f"Testing {case['hours']} hours in first range"):
                result: float = PaymentService.calculate_payment(case["hours"])
                self.assertEqual(result, case["expected_payment"])

    def test_calculate_payment_second_range_limits(self) -> None:
        """
        Verifica el cálculo para los límites del segundo rango (15-28 horas).
        """
        test_cases: List[Dict[str, int]] = [
            {"hours": 15, "expected_payment": 3150},
            {"hours": 28, "expected_payment": 5880},
        ]
        for case in test_cases:
            with self.subTest(f"Testing {case['hours']} hours in second range"):
                result: float = PaymentService.calculate_payment(case["hours"])
                self.assertEqual(result, case["expected_payment"])

    def test_calculate_payment_third_range_limits(self) -> None:
        """
        Verifica el cálculo para los límites del tercer rango (29-47 horas).
        """
        test_cases: List[Dict[str, int]] = [
            {"hours": 29, "expected_payment": 7221},
            {"hours": 47, "expected_payment": 11703},
        ]
        for case in test_cases:
            with self.subTest(f"Testing {case['hours']} hours in third range"):
                result: float = PaymentService.calculate_payment(case["hours"])
                self.assertEqual(result, case["expected_payment"])

    def test_calculate_payment_fourth_range_limits(self) -> None:
        """
        Verifica el cálculo para los límites del cuarto rango (48+ horas).
        """
        test_cases: List[Dict[str, int]] = [
            {"hours": 48, "expected_payment": 13776},
            {"hours": 100, "expected_payment": 28700},
        ]
        for case in test_cases:
            with self.subTest(f"Testing {case['hours']} hours in fourth range"):
                result: float = PaymentService.calculate_payment(case["hours"])
                self.assertEqual(result, case["expected_payment"])

    def test_calculate_payment_invalid_hours(self) -> None:
        """
        Verifica que se lance una excepción para horas fuera de rango.
        """
        invalid_hours: List[int] = [-5, -1, -100]
        for hours in invalid_hours:
            with self.subTest(f"Testing invalid hours: {hours}"):
                with self.assertRaises(ValueError):
                    PaymentService.calculate_payment(hours)


if __name__ == "__main__":
    unittest.main()
