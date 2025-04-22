from typing import Any, Dict, List

from django.db.models import Count, Q, QuerySet, Sum
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.technician.services.payment_service import PaymentService
from rapihogar.models import Technician


class TechnicianPaymentView(APIView):
    """
    Endpoint para listar técnicos y calcular el pago según las horas trabajadas.
    Permite filtrar por parte del nombre.
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Devuelve una lista de técnicos con sus datos calculados.
        """

        name_filter: str = request.query_params.get("name", "")
        technicians: QuerySet = Technician.objects.filter(
            Q(first_name__icontains=name_filter) | Q(last_name__icontains=name_filter)
        ).annotate(
            total_hours=Sum("order__hours_worked"),
            total_orders=Count("order"),
        )

        default_hours: int = 0
        data: List[Dict[str, Any]] = [
            {
                "full_name": technician.full_name,
                "total_hours": technician.total_hours or default_hours,
                "total_payment": round(
                    PaymentService.calculate_payment(
                        technician.total_hours or default_hours
                    ),
                    2,
                ),
                "total_orders": technician.total_orders,
            }
            for technician in technicians
        ]

        return Response(data)
