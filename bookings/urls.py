from django.urls import path, include
from .views import HomeView, DashboardView, AppointmentCreateView, AppointmentSuccessView, AppointmentDetailView, BookedTimesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/appointments/<int:pk>/", AppointmentDetailView.as_view(), name="appointment_detail"),
    path('book/', AppointmentCreateView.as_view(), name="appointment_create"),
    path("booking/success/<uuid:token>/", AppointmentSuccessView.as_view(), name="appointment_success"),
    path("booked-times/", BookedTimesView.as_view(), name="booked_times"),
]