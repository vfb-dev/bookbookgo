from django.urls import path, include
from .views import AppointmentCreateView, AppointmentSuccessView, BookedTimesView

urlpatterns = [
    path('book/', AppointmentCreateView.as_view(), name="appointment_create"),
    path("booking/success/", AppointmentSuccessView.as_view(), name="appointment_success"),

    path("booked-times/", BookedTimesView.as_view(), name="booked_times"),
]