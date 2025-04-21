from django.urls import include, path
from rest_framework import routers

from api.technician.views import TechnicianListView

from .company.views import CompanyViewSet

router = routers.DefaultRouter()
router.register(r"company", CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),
    path("technicians/", TechnicianListView.as_view(), name="technician-list"),
]
