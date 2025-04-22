from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.order.serializers import OrderUpdateSerializer
from rapihogar.models import Pedido


class OrderUpdateView(APIView):
    """
    Servicio para modificar solo los pedidos.
    """

    def patch(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        """
        Actualiza un pedido existente.
        """
        order: Pedido = get_object_or_404(Pedido, pk=pk)
        serializer: OrderUpdateSerializer = OrderUpdateSerializer(
            order, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
