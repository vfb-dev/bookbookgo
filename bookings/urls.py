from django.urls import path, include
from .views import HomeView, AppointmentCreateView, AppointmentSuccessView, BookedTimesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('book/', AppointmentCreateView.as_view(), name="appointment_create"),
    path("booking/success/<int:pk>/", AppointmentSuccessView.as_view(), name="appointment_success"),
    path("booked-times/", BookedTimesView.as_view(), name="booked_times"),
]