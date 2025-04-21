from typing import Any, Dict, List

from django.db.models import Count, Q, QuerySet, Sum
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.technician.serializers import TechnicianSerializer
from api.technician.services.payment_service import PaymentService
from rapihogar.models import Technician


class TechnicianListView(ListAPIView):
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
