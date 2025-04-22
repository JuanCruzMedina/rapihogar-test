from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from rapihogar.models import Technician


@dataclass(frozen=True)
class TechnicianPayment:
    """Clase que representa el pago de un técnico."""

    technician: Technician
    total_payment: float

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto TechnicianPayment a un diccionario.
        """
        return {
            "technician_id": self.technician.id,
            "full_name": f"{self.technician.first_name} {self.technician.last_name}",
            "total_payment": round(self.total_payment, 2),
        }


@dataclass(frozen=True)
class TechniciansPayments:
    """
    Esta clase se encarga de calcular el pago total y las horas trabajadas
    de cada técnico, así como de generar informes relacionados con los
    pagos de los técnicos.
    """

    technicians_payments: List[TechnicianPayment]

    def get_average_payment(self) -> float:
        """
        Calcula el monto promedio cobrado por todos los técnicos.
        """
        total_payments = [
            technician_payment.total_payment
            for technician_payment in self.technicians_payments
        ]
        default_average: float = 0.0
        return (
            sum(total_payments) / len(total_payments)
            if total_payments
            else default_average
        )

    def get_below_average_technicians(
        self, average_payment: float
    ) -> List[TechnicianPayment]:
        """
        Devuelve una lista de técnicos que cobraron menos que el promedio.
        """
        return [
            technician_payment
            for technician_payment in self.technicians_payments
            if technician_payment.total_payment < average_payment
        ]

    def get_lowest_paid_technician(self) -> Optional[TechnicianPayment]:
        """
        Devuelve el técnico con el monto más bajo.
        """
        return min(
            self.technicians_payments,
            key=lambda technician_payment: (
                technician_payment.total_payment,
                -technician_payment.technician.id,
            ),
            default=None,
        )

    def get_highest_paid_technician(self) -> Optional[TechnicianPayment]:
        """
        Devuelve el técnico con el monto más alto.
        """
        return max(
            self.technicians_payments,
            key=lambda technician_payment: (
                technician_payment.total_payment,
                -technician_payment.technician.id,
            ),
            default=None,
        )
