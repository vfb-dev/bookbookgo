from django.shortcuts import render, redirect
from django.views import View
from .forms import AppointmentForm
from .models import Appointment
from django.http import JsonResponse

# Create your views here.
class AppointmentCreateView(View):
    def get(self, request):
        form = AppointmentForm()
        return render(request, "bookings/appointment_form.html", {"form": form})

    def post(self, request):
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("appointment_success")

        return render(request, "bookings/appointment_form.html", {"form": form})
    
class AppointmentSuccessView(View):
    def get(self, request):
        return render(request, "bookings/appointment_success.html")
    
class BookedTimesView(View):
    def get(self, request):
        appointment_date = request.GET.get("date")

        booked_times = Appointment.objects.filter(
            appointment_date=appointment_date
        ).values_list("appointment_time", flat=True)

        data = [time.strftime("%H:%M:%S") for time in booked_times]

        return JsonResponse({"booked_times": data})