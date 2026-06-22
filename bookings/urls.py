from django.urls import path, include
from .views import AppointmentCreateView

urlpatterns = [
    path('book/', AppointmentCreateView.as_view(), name="appointment_create"),
]