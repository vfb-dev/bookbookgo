from django.urls import path, include
from .views import AppointmentCreateView, AppointmentSuccessView

urlpatterns = [
    path('book/', AppointmentCreateView.as_view(), name="appointment_create"),
    path("booking/success/", AppointmentSuccessView.as_view(), name="appointment_success"),
]