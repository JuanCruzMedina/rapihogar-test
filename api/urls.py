from django.urls import include, path
from rest_framework import routers

from api.order.views import OrderUpdateView
from api.technician.views import TechnicianPaymentListView, TechnicianReportView

from .company.views import CompanyViewSet

router = routers.DefaultRouter()
router.register(r"company", CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "technicians/payments/",
        TechnicianPaymentListView.as_view(),
        name="technician-payments-list",
    ),
    path(
        "technicians/report/", TechnicianReportView.as_view(), name="technician-report"
    ),
    path("order/<int:pk>/", OrderUpdateView.as_view(), name="order-update"),
]
