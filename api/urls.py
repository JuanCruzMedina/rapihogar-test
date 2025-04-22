from django.urls import include, path
from rest_framework import routers

from api.company.views.company_view import CompanyViewSet
from api.order.views.update_view import OrderUpdateView
from api.technician.views.payment_view import TechnicianPaymentView
from api.technician.views.report_view import TechnicianReportView

router = routers.DefaultRouter()
router.register(r"company", CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "technicians/payments/",
        TechnicianPaymentView.as_view(),
        name="technician-payments-list",
    ),
    path(
        "technicians/report/", TechnicianReportView.as_view(), name="technician-report"
    ),
    path("order/<int:pk>/", OrderUpdateView.as_view(), name="order-update"),
]
