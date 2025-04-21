from typing import List


class PaymentService:
    """
    Servicio para calcular el pago de un técnico según las horas trabajadas.
    """

    RATE_CONFIG: List[dict] = [
        {"min_hours": 0, "max_hours": 14, "rate": 200, "discount": 0.15},
        {"min_hours": 15, "max_hours": 28, "rate": 250, "discount": 0.16},
        {"min_hours": 29, "max_hours": 47, "rate": 300, "discount": 0.17},
        {"min_hours": 48, "max_hours": float("inf"), "rate": 350, "discount": 0.18},
    ]

    @staticmethod
    def get_rate_config(total_hours: int) -> dict:
        """
        Encuentra la configuración de tarifa correspondiente al número de horas trabajadas.
        """
        if not isinstance(total_hours, int):
            raise ValueError("El número de horas trabajadas debe ser un entero.")

        for config in PaymentService.RATE_CONFIG:
            if config["min_hours"] <= total_hours <= config["max_hours"]:
                return config
        raise ValueError("Horas trabajadas fuera de los rangos definidos.")

    @staticmethod
    def calculate_payment(total_hours: int) -> float:
        """
        Calcula el pago total según la configuración de tarifa.
        """
        config = PaymentService.get_rate_config(total_hours)
        gross_payment: float = total_hours * config["rate"]
        total_payment: float = gross_payment - (gross_payment * config["discount"])
        return total_payment
