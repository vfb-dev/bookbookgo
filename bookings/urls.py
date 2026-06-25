from django.urls import path, include
from .views import (
    AppointmentCreateView,
    AppointmentDetailView,
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
    path("booked-times/", BookedTimesView.as_view(), name="booked_times"),
]