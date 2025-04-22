from typing import Any, Dict, List, Optional

from django.db.models import Count, Q, QuerySet, Sum
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.technician.serializers import TechnicianSerializer
from api.technician.services.payment_service import PaymentService
from rapihogar.models import Technician


class TechnicianPaymentListView(ListAPIView):  # TODO: change to APIView
    """
    Endpoint para listar técnicos y calcular el pago según las horas trabajadas.
    Permite filtrar por parte del nombre.
    """

    queryset: QuerySet = Technician.objects.all()
    serializer_class = TechnicianSerializer

    def get_queryset(self) -> QuerySet:
        """
        Filtra técnicos por el nombre o apellido y anota datos adicionales.
        """
        name_filter: str = self.request.query_params.get("name", "")
        return Technician.objects.filter(
            Q(first_name__icontains=name_filter) | Q(last_name__icontains=name_filter)
        ).annotate(
            total_hours=Sum("pedido__hours_worked"),
            total_orders=Count("pedido"),
        )

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Devuelve una lista de técnicos con sus datos calculados.
        """
        queryset: QuerySet = self.get_queryset()
        data: List[Dict[str, Any]] = []

        for technician in queryset:
            total_hours: int = technician.total_hours or 0
            total_payment: float = PaymentService.calculate_payment(total_hours)
            data.append(
                {
                    "full_name": f"{technician.first_name} {technician.last_name}",
                    "total_hours": total_hours,
                    "total_payment": round(total_payment, 2),
                    "total_orders": technician.total_orders,
                }
            )
        return Response(data)


class TechnicianReportView(APIView):
    """
    Vista para generar un informe de técnicos.
    """

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        technicians: QuerySet = Technician.objects.annotate(
            total_hours=Sum("pedido__hours_worked"),
            total_orders=Count("pedido"),
        )

        technicians_data: List[Dict[str, Any]] = [
            {
                "technician": technician,
                "full_name": f"{technician.first_name} {technician.last_name}",
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
