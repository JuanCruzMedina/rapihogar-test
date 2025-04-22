from typing import Any, Dict, List, Optional

from django.db.models import Count, QuerySet, Sum
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.technician.services.payment_service import PaymentService
from rapihogar.models import Technician


class TechnicianReportView(APIView):
    """
    Vista para generar un informe de técnicos.
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        technicians: QuerySet = Technician.objects.annotate(
            total_hours=Sum("order__hours_worked"),
            total_orders=Count("order"),
        )

        technicians_data: List[Dict[str, Any]] = [
            {
                "technician": technician,
                "full_name": technician.full_name,
                "total_hours": technician.total_hours or 0,
                "total_payment": PaymentService.calculate_payment(
                    technician.total_hours or 0
                ),
            }
            for technician in technicians
        ]
        total_payments: List[float] = [
            data["total_payment"] for data in technicians_data
        ]
        average_payment: float = (
            sum(total_payments) / len(total_payments) if total_payments else 0
        )

        below_average_technicians: List[Dict[str, Any]] = [
            {
                "full_name": technician_data["full_name"],
                "total_payment": technician_data["total_payment"],
            }
            for technician_data in technicians_data
            if technician_data["total_payment"] < average_payment
        ]

        lowest_paid_technician: Optional[Dict[str, Any]] = min(
            technicians_data,
            key=lambda data: (data["total_payment"], -data["technician"].id),
            default=None,
        )

        highest_paid_technician: Optional[Dict[str, Any]] = max(
            technicians_data,
            key=lambda data: (data["total_payment"], -data["technician"].id),
            default=None,
        )

        data: Dict[str, Any] = {
            "average_payment": round(average_payment, 2),
            "below_average_technicians": below_average_technicians,
            "lowest_paid_technician": (
                {
                    "full_name": lowest_paid_technician["full_name"],
                    "total_payment": lowest_paid_technician["total_payment"],
                }
                if lowest_paid_technician
                else None
            ),
            "highest_paid_technician": (
                {
                    "full_name": highest_paid_technician["full_name"],
                    "total_payment": highest_paid_technician["total_payment"],
                }
                if highest_paid_technician
                else None
            ),
        }

        return Response(data)
