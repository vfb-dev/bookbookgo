from django.urls import path, include
from .views import (
    AppointmentCreateView,
    AppointmentCancelView,
    AppointmentDetailView,
    AppointmentRescheduleView,
    AppointmentSuccessView,
    BookedTimesView,
    ContactView,
    DashboardView,
    HomeView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment_detail"),
    path('book/', AppointmentCreateView.as_view(), name="appointment_create"),
    path("booking/success/<uuid:token>/", AppointmentSuccessView.as_view(), name="appointment_success"),
    path("booking/<uuid:token>/reschedule/", AppointmentRescheduleView.as_view(), name="appointment_reschedule"),
    path("booking/<uuid:token>/cancel/", AppointmentCancelView.as_view(), name="appointment_cancel"),
    path("booked-times/", BookedTimesView.as_view(), name="booked_times"),
]
