from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .forms import AppointmentForm
from .models import Appointment

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, "bookings/home.html")
    
class DashboardView(LoginRequiredMixin, View):
    login_url = "/admin/login/"

    def get(self, request):
        today = timezone.localdate()

        appointments = Appointment.objects.filter(
            appointment_date__gte=today
        ).order_by("appointment_date", "appointment_time")

        context = {
            "total_appointments": Appointment.objects.count(),
            "pending_appointments": Appointment.objects.filter(status="pending").count(),
            "confirmed_appointments": Appointment.objects.filter(status="confirmed").count(),
            "upcoming_appointments": appointments,
        }

        return render(request, "bookings/dashboard.html", context)

class AppointmentCreateView(View):
    def get(self, request):
        form = AppointmentForm()
        return render(request, "bookings/appointment_form.html", {"form": form})

    def post(self, request):
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save()
            return redirect("appointment_success", pk=appointment.pk)

        return render(request, "bookings/appointment_form.html", {"form": form})
    
class AppointmentSuccessView(View):
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        return render(
            request,
            "bookings/appointment_success.html",
            {"appointment": appointment},
        )
    
class AppointmentDetailView(LoginRequiredMixin, View):
    login_url = "/admin/login/"

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)

        return render(
            request,
            "bookings/appointment_detail.html",
            {"appointment": appointment},
        )
    
class BookedTimesView(View):
    def get(self, request):
        appointment_date = request.GET.get("date")

        booked_times = Appointment.objects.filter(
            appointment_date=appointment_date
        ).values_list("appointment_time", flat=True)

        data = [time.strftime("%H:%M:%S") for time in booked_times]

        return JsonResponse({"booked_times": data})