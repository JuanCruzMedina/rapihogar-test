from rest_framework import serializers


class TechnicianSerializer(serializers.Serializer):
    """
    Serializador para la lista de técnicos.
    Este serializador se utiliza para mostrar el nombre completo del técnico,
    el total de horas trabajadas, el total de pedidos y el pago total.
    """

    full_name = serializers.CharField()
    total_hours = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    total_payment = serializers.FloatField()
