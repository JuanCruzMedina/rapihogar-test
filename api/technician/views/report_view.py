from typing import Any, Dict, List, Optional

from django.db.models import Count, QuerySet, Sum
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.technician.services.payment_service import PaymentService
from api.technician.value_objects import TechnicianPayment, TechniciansPayments
from rapihogar.models import Technician


class TechnicianReportView(APIView):
    """
    Vista para generar un informe de técnicos.
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        technician_queryset: QuerySet = Technician.objects.annotate(
            total_hours=Sum("order__hours_worked")
        )

        default_hours: int = 0
        technicians_payments_data: List[TechnicianPayment] = [
            TechnicianPayment(
                technician=technician,
                total_payment=PaymentService.calculate_payment(
                    technician.total_hours or default_hours
                ),
            )
            for technician in technician_queryset
        ]
        technicians = TechniciansPayments(technicians_payments_data)
        average_payment: float = technicians.get_average_payment()
        below_average_technicians: List[TechnicianPayment] = (
            technicians.get_below_average_technicians(average_payment)
        )
        lowest_paid_technician: Optional[TechnicianPayment] = (
            technicians.get_lowest_paid_technician()
        )
        highest_paid_technician: Optional[TechnicianPayment] = (
            technicians.get_highest_paid_technician()
        )

        data = {
            "average_payment": round(average_payment, 2),
            "below_average_technicians": [
                technician_payment.to_dict()
                for technician_payment in below_average_technicians
            ],
            "lowest_paid_technician": (
                lowest_paid_technician.to_dict() if lowest_paid_technician else None
            ),
            "highest_paid_technician": (
                highest_paid_technician.to_dict() if highest_paid_technician else None
            ),
        }

        return Response(data)
