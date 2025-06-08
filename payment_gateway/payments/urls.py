from django.urls import path
from .views import InitiatePaymentView, PaymentStatusView

app_name = "api"

urlpatterns = [
    path("payments", InitiatePaymentView.as_view(), name="initiate_payment"),
    path("payments/<str:payment_id>", PaymentStatusView.as_view(), name="payment_status"),
]
