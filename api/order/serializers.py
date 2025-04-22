from typing import Any, Dict

from rest_framework import serializers

from rapihogar.models import Pedido


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar un pedido existente.
    Este serializador permite modificar los campos `client`, `scheme`, `technician` y `hours_worked`
    de un pedido existente. Se asegura de que el pedido a modificar sea de tipo "PEDIDO".
    Si el pedido no es de tipo "PEDIDO", se lanzará una excepción de validación.
    """

    class Meta:
        model = Pedido
        fields = ["client", "scheme", "technician", "hours_worked"]

    def validate_hours_worked(self, value: int) -> int:
        """
        Valida que el valor de `hours_worked` no sea negativo.

        Args:
            value (int): El valor de horas trabajadas.

        Raises:
            serializers.ValidationError: Si el valor es negativo.

        Returns:
            int: El valor validado de horas trabajadas.
        """
        if value < 0:
            raise serializers.ValidationError(
                "El valor de hours_worked no puede ser negativo."
            )
        return value

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida que el pedido a modificar sea de tipo "PEDIDO".

        Args:
            data (Dict[str, Any]): Los datos del pedido a validar.

        Raises:
            serializers.ValidationError: Si el tipo de pedido no es "PEDIDO".

        Returns:
            Dict[str, Any]: Los datos validados del pedido.
        """
        if self.instance.type_request != Pedido.PEDIDO:
            raise serializers.ValidationError("Solo se pueden modificar pedidos")
        return data
