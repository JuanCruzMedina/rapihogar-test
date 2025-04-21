from rest_framework import viewsets

from api.company.serializers import CompanySerializer
from rapihogar.models import Company


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.filter()
